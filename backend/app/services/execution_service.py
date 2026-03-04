import docker
import tempfile
import os
import time
from typing import Dict, Optional
from app.config import settings


class ExecutionResult:
    """Container for execution results"""
    def __init__(
        self,
        verdict: str,
        output: Optional[str] = None,
        runtime: Optional[float] = None,
        memory: Optional[float] = None,
        error: Optional[str] = None,
    ):
        self.verdict = verdict
        self.output = output
        self.runtime = runtime
        self.memory = memory
        self.error = error


class ExecutionService:
    """Execute code in isolated Docker containers"""
    
    LANGUAGE_CONFIGS = {
        "python": {
            "image": "python:3.11-slim",
            "extension": ".py",
            "command": "python /code/solution.py",
        },
        "cpp": {
            "image": "gcc:13",
            "extension": ".cpp",
            "command": "sh -c 'g++ -o /code/solution /code/solution.cpp && /code/solution'",
        },
        "java": {
            "image": "openjdk:17-slim",
            "extension": ".java",
            "command": "sh -c 'javac /code/Solution.java && java -cp /code Solution'",
        },
        "javascript": {
            "image": "node:20-slim",
            "extension": ".js",
            "command": "node /code/solution.js",
        },
    }
    
    def __init__(self):
        self.client = docker.from_env()
        self.timeout = settings.EXECUTION_TIMEOUT
        self.memory_limit = settings.DOCKER_MEMORY_LIMIT
        self.cpu_limit = settings.DOCKER_CPU_LIMIT
    
    async def execute_code(
        self, code: str, language: str, test_input: str = ""
    ) -> ExecutionResult:
        """Execute code in isolated Docker container"""
        
        language = language.lower()
        if language not in self.LANGUAGE_CONFIGS:
            return ExecutionResult(
                verdict="Runtime Error",
                error=f"Unsupported language: {language}",
            )
        
        config = self.LANGUAGE_CONFIGS[language]
        
        # Create temporary directory for code
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write code to file
            filename = "Solution.java" if language == "java" else f"solution{config['extension']}"
            code_path = os.path.join(tmpdir, filename)
            
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # Create input file if needed
            if test_input:
                input_path = os.path.join(tmpdir, "input.txt")
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(test_input)
            
            try:
                # Pull image if not exists
                try:
                    self.client.images.get(config["image"])
                except docker.errors.ImageNotFound:
                    self.client.images.pull(config["image"])
                
                # Run container
                start_time = time.time()
                
                container = self.client.containers.run(
                    config["image"],
                    command=config["command"],
                    volumes={tmpdir: {"bind": "/code", "mode": "ro"}},
                    network_mode="none",  # No network access
                    mem_limit=self.memory_limit,
                    cpu_quota=int(self.cpu_limit * 100000),
                    cpu_period=100000,
                    user="nobody",  # Non-root user
                    detach=True,
                    remove=False,
                )
                
                try:
                    # Wait for container with timeout
                    result = container.wait(timeout=self.timeout)
                    runtime = (time.time() - start_time) * 1000  # Convert to ms
                    
                    # Get output
                    output = container.logs().decode("utf-8", errors="ignore")
                    
                    # Get memory stats
                    stats = container.stats(stream=False)
                    memory_usage = stats["memory_stats"].get("usage", 0) / (1024 * 1024)  # Convert to MB
                    
                    # Determine verdict
                    exit_code = result["StatusCode"]
                    
                    if exit_code == 0:
                        verdict = "Accepted"  # Base verdict, will be checked against expected output
                    else:
                        verdict = "Runtime Error"
                    
                    return ExecutionResult(
                        verdict=verdict,
                        output=output,
                        runtime=round(runtime, 2),
                        memory=round(memory_usage, 2),
                    )
                
                except docker.errors.ContainerError as e:
                    return ExecutionResult(
                        verdict="Runtime Error",
                        error=str(e),
                    )
                
                except Exception as e:
                    if "timeout" in str(e).lower():
                        return ExecutionResult(
                            verdict="Time Limit Exceeded",
                            runtime=self.timeout * 1000,
                        )
                    return ExecutionResult(
                        verdict="Runtime Error",
                        error=str(e),
                    )
                
                finally:
                    # Cleanup container
                    try:
                        container.stop(timeout=1)
                        container.remove()
                    except:
                        pass
            
            except Exception as e:
                return ExecutionResult(
                    verdict="Runtime Error",
                    error=f"Execution failed: {str(e)}",
                )
    
    def __del__(self):
        """Cleanup Docker client"""
        try:
            self.client.close()
        except:
            pass
