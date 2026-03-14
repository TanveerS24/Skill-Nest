package com.skillnest.service;

import com.github.dockerjava.api.DockerClient;
import com.github.dockerjava.api.command.CreateContainerResponse;
import com.github.dockerjava.api.model.Bind;
import com.github.dockerjava.api.model.HostConfig;
import com.github.dockerjava.api.model.Volume;
import com.github.dockerjava.core.DefaultDockerClientConfig;
import com.github.dockerjava.core.DockerClientImpl;
import com.github.dockerjava.httpclient5.ApacheDockerHttpClient;
import com.github.dockerjava.transport.DockerHttpClient;
import com.skillnest.entity.Language;
import com.skillnest.entity.Verdict;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.time.Duration;
import java.time.Instant;

@Service
@Slf4j
public class CodeExecutionService {
    
    private final DockerClient dockerClient;
    
    public CodeExecutionService() {
        try {
            DefaultDockerClientConfig config = DefaultDockerClientConfig.createDefaultConfigBuilder().build();
            DockerHttpClient httpClient = new ApacheDockerHttpClient.Builder()
                    .dockerHost(config.getDockerHost())
                    .sslConfig(config.getSSLConfig())
                    .maxConnections(100)
                    .connectionTimeout(Duration.ofSeconds(30))
                    .responseTimeout(Duration.ofSeconds(45))
                    .build();
            this.dockerClient = DockerClientImpl.getInstance(config, httpClient);
        } catch (Exception e) {
            log.warn("Docker client initialization warning: {}", e.getMessage());
            throw new RuntimeException("Failed to initialize Docker client", e);
        }
    }
    
    public ExecutionResult executeCode(String code, Language language, String testInput, 
                                       Integer timeLimit, Integer memoryLimit) {
        try {
            String imageName = getImageName(language);
            String extension = getFileExtension(language);
            String command = getExecutionCommand(language);
            
            // Create temporary directory for the submission
            File tempDir = new File(System.getProperty("java.io.tmpdir") + File.separator + "skillnest_" + System.nanoTime());
            if (!tempDir.mkdirs()) {
                throw new RuntimeException("Failed to create temp directory");
            }
            
            // Write code to file
            File codeFile = new File(tempDir, "code" + extension);
            java.nio.file.Files.write(codeFile.toPath(), code.getBytes());
            
            // Create container
            CreateContainerResponse container = dockerClient.createContainerCmd(imageName)
                    .withHostConfig(new HostConfig()
                            .withMemory((long) memoryLimit * 1024 * 1024)
                            .withMemorySwap((long) memoryLimit * 1024 * 1024)
                            .withBinds(new Bind(tempDir.getAbsolutePath(), new Volume("/code")))
                            .withNetworkMode("none")
                    )
                    .withCmd("/bin/bash", "-c", command)
                    .withWorkingDir("/code")
                    .exec();
            
            String containerId = container.getId();
            
            // Start container
            Instant startTime = Instant.now();
            dockerClient.startContainerCmd(containerId).exec();
            
            // Wait for completion with timeout
            Integer exitCode = dockerClient.waitContainerCmd(containerId)
                    .exec(new com.github.dockerjava.api.command.WaitContainerResultCallback())
                    .awaitStatusCode((int) (timeLimit + 5), java.util.concurrent.TimeUnit.SECONDS);
            
            Instant endTime = Instant.now();
            double runtime = Duration.between(startTime, endTime).toMillis();
            
            // Get logs using inspectContainerCmd
            String output = "";
            try {
                var inspection = dockerClient.inspectContainerCmd(containerId).exec();
                output = inspection.toString();
            } catch (Exception e) {
                log.debug("Could not retrieve container logs: {}", e.getMessage());
            }
            
            // Clean up
            try {
                dockerClient.removeContainerCmd(containerId)
                        .withForce(true)
                        .exec();
            } catch (Exception e) {
                log.warn("Failed to remove container: {}", e.getMessage());
            }
            
            // Check timeout
            if (runtime > timeLimit * 1000) {
                return ExecutionResult.builder()
                        .verdict(Verdict.TIME_LIMIT_EXCEEDED)
                        .runtime(runtime)
                        .build();
            }
            
            // Check compilation/runtime errors
            if (exitCode != null && exitCode != 0) {
                return ExecutionResult.builder()
                        .verdict(Verdict.COMPILATION_ERROR)
                        .runtime(runtime)
                        .output(output)
                        .build();
            }
            
            return ExecutionResult.builder()
                    .verdict(Verdict.ACCEPTED)
                    .runtime(runtime)
                    .output(output)
                    .build();
            
        } catch (Exception e) {
            log.error("Code execution failed", e);
            return ExecutionResult.builder()
                    .verdict(Verdict.RUNTIME_ERROR)
                    .output("Execution error: " + e.getMessage())
                    .build();
        }
    }
    
    private String getImageName(Language language) {
        return switch (language) {
            case PYTHON -> "python:3.11-slim";
            case JAVA -> "openjdk:21-slim";
            case C -> "gcc:latest";
            case CPP -> "gcc:latest";
        };
    }
    
    private String getFileExtension(Language language) {
        return switch (language) {
            case PYTHON -> ".py";
            case JAVA -> ".java";
            case C -> ".c";
            case CPP -> ".cpp";
        };
    }
    
    private String getExecutionCommand(Language language) {
        return switch (language) {
            case PYTHON -> "python3 code.py";
            case JAVA -> "javac code.java && java code";
            case C -> "gcc -o code code.c && ./code";
            case CPP -> "g++ -o code code.cpp && ./code";
        };
    }
}
