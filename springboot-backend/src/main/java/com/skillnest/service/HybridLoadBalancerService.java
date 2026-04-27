package com.skillnest.service;

import com.skillnest.dto.ExecutionRequest;
import com.skillnest.entity.Language;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.concurrent.TimeUnit;

@Service
@Slf4j
public class HybridLoadBalancerService {
    
    private static final String REQUEST_COUNT_PREFIX = "loadbalancer:request_count:";
    private static final String EXECUTION_ENDPOINT = "/api/execute";
    private static final int MAX_RETRIES = 2;
    private static final int REQUEST_COUNT_TTL_MINUTES = 5;
    
    @Autowired
    private ManualLoadBalancer manualLoadBalancer;
    
    @Autowired
    private HealthCheckService healthCheckService;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Autowired
    private RestTemplate restTemplate;
    
    public ExecutionResult executeWithLoadBalancing(String code, Language language, 
                                                     String testInput, Integer timeLimit, Integer memoryLimit) {
        if (!manualLoadBalancer.isEnabled() || manualLoadBalancer.getInstanceCount() == 0) {
            log.info("Load balancer disabled or no instances configured, executing locally");
            return executeLocally(code, language, testInput, timeLimit, memoryLimit);
        }
        
        List<String> healthyInstances = healthCheckService.getHealthyInstances(
            manualLoadBalancer.getAllInstances());
        
        if (healthyInstances.isEmpty()) {
            log.warn("No healthy instances available, falling back to local execution");
            return executeLocally(code, language, testInput, timeLimit, memoryLimit);
        }
        
        return executeWithRetry(code, language, testInput, timeLimit, memoryLimit, healthyInstances);
    }
    
    private ExecutionResult executeWithRetry(String code, Language language, 
                                            String testInput, Integer timeLimit, Integer memoryLimit,
                                            List<String> healthyInstances) {
        int attempt = 0;
        Exception lastException = null;
        
        while (attempt <= MAX_RETRIES) {
            String instanceUrl;
            
            if (attempt == 0) {
                instanceUrl = manualLoadBalancer.getNextInstanceRoundRobin();
                if (!healthyInstances.contains(instanceUrl)) {
                    instanceUrl = healthyInstances.get(0);
                }
            } else {
                int fallbackIndex = attempt % healthyInstances.size();
                instanceUrl = healthyInstances.get(fallbackIndex);
            }
            
            log.info("Attempt {}/{}: Executing on instance {}", attempt + 1, MAX_RETRIES + 1, instanceUrl);
            
            try {
                incrementRequestCount(instanceUrl);
                ExecutionResult result = executeOnInstance(instanceUrl, code, language, 
                    testInput, timeLimit, memoryLimit);
                
                log.info("Successfully executed on instance: {}", instanceUrl);
                return result;
                
            } catch (Exception e) {
                lastException = e;
                log.error("Execution failed on instance {}: {}", instanceUrl, e.getMessage());
                healthCheckService.markInstanceUnhealthy(instanceUrl);
                attempt++;
            }
        }
        
        log.error("All retries exhausted, falling back to local execution");
        return executeLocally(code, language, testInput, timeLimit, memoryLimit);
    }
    
    private ExecutionResult executeOnInstance(String instanceUrl, String code, Language language,
                                             String testInput, Integer timeLimit, Integer memoryLimit) {
        try {
            String executionUrl = instanceUrl + EXECUTION_ENDPOINT;
            
            ExecutionRequest request = ExecutionRequest.builder()
                .code(code)
                .language(language)
                .input(testInput)
                .timeLimit(timeLimit)
                .memoryLimit(memoryLimit)
                .build();
            
            ExecutionResult response = restTemplate.postForObject(executionUrl, request, ExecutionResult.class);
            
            if (response == null) {
                throw new RuntimeException("Null response from instance: " + instanceUrl);
            }
            
            return response;
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to execute on instance " + instanceUrl + ": " + e.getMessage(), e);
        }
    }
    
    private ExecutionResult executeLocally(String code, Language language,
                                          String testInput, Integer timeLimit, Integer memoryLimit) {
        CodeExecutionService localExecutor = new CodeExecutionService();
        return localExecutor.executeCode(code, language, testInput, timeLimit, memoryLimit);
    }
    
    private void incrementRequestCount(String instanceUrl) {
        try {
            String key = REQUEST_COUNT_PREFIX + instanceUrl;
            redisTemplate.opsForValue().increment(key);
            redisTemplate.expire(key, REQUEST_COUNT_TTL_MINUTES, TimeUnit.MINUTES);
        } catch (Exception e) {
            log.debug("Failed to increment request count for {}: {}", instanceUrl, e.getMessage());
        }
    }
    
    public long getRequestCount(String instanceUrl) {
        try {
            String key = REQUEST_COUNT_PREFIX + instanceUrl;
            Long count = (Long) redisTemplate.opsForValue().get(key);
            return count != null ? count : 0;
        } catch (Exception e) {
            log.debug("Failed to get request count for {}: {}", instanceUrl, e.getMessage());
            return 0;
        }
    }
    
    public String getLeastLoadedInstance(List<String> instances) {
        return instances.stream()
            .min((a, b) -> Long.compare(getRequestCount(a), getRequestCount(b)))
            .orElse(instances.get(0));
    }
}
