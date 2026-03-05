import docker
import tempfile
import os
import time
from typing import Dict, Optional
from app.models import Language, Verdict
from app.schemas import ExecutionResult
import asyncio
import psutil


class DockerExecutor:
    def __init__(self):
        self._client = None
        self.language_configs = {
            Language.PYTHON: {
                "image": "python:3.11-slim",
                "file_extension": "py",
                "compile_cmd": None,
                "run_cmd": "python solution.py"
            },
            Language.JAVA: {
                "image": "openjdk:17-slim",
                "file_extension": "java",
                "compile_cmd": "javac Solution.java",
                "run_cmd": "java Solution"
            },
            Language.C: {
                "image": "gcc:13-alpine",
                "file_extension": "c",
                "compile_cmd": "gcc solution.c -o solution",
                "run_cmd": "./solution"
            },
            Language.CPP: {
                "image": "gcc:13-alpine",
                "file_extension": "cpp",
                "compile_cmd": "g++ solution.cpp -o solution",
                "run_cmd": "./solution"
            }
        }
    
    @property
    def client(self):
        """Lazy initialization of Docker client"""
        if self._client is None:
            try:
                self._client = docker.from_env()
            except Exception as e:
                raise RuntimeError(f"Failed to connect to Docker daemon: {e}. "
                                 "Make sure Docker is running and the socket is mounted.")
        return self._client
    
    async def execute_code(
        self,
        code: str,
        language: Language,
        test_input: str,
        time_limit: int,
        memory_limit: int
    ) -> ExecutionResult:
        """Execute code in isolated Docker container"""
        config = self.language_configs.get(language)
        if not config:
            return ExecutionResult(
                verdict=Verdict.RUNTIME_ERROR,
                error="Unsupported language"
            )
        
        # Create temporary directory for code
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write code to file
            file_name = f"Solution.{config['file_extension']}" if language == Language.JAVA else f"solution.{config['file_extension']}"
            file_path = os.path.join(temp_dir, file_name)
            
            with open(file_path, "w") as f:
                f.write(code)
            
            # Write input to file
            input_path = os.path.join(temp_dir, "input.txt")
            with open(input_path, "w") as f:
                f.write(test_input)
            
            try:
                # Compile if necessary
                if config["compile_cmd"]:
                    compile_result = await self._run_container(
                        image=config["image"],
                        command=config["compile_cmd"],
                        volumes={temp_dir: {"bind": "/workspace", "mode": "rw"}},
                        working_dir="/workspace",
                        timeout=10,
                        memory_limit=f"{memory_limit}m"
                    )
                    
                    if compile_result["status_code"] != 0:
                        return ExecutionResult(
                            verdict=Verdict.COMPILATION_ERROR,
                            error=compile_result["error"]
                        )
                
                # Run code
                start_time = time.time()
                run_result = await self._run_container(
                    image=config["image"],
                    command=f"{config['run_cmd']} < input.txt",
                    volumes={temp_dir: {"bind": "/workspace", "mode": "ro"}},
                    working_dir="/workspace",
                    timeout=time_limit,
                    memory_limit=f"{memory_limit}m"
                )
                execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Check verdict
                if run_result["timeout"]:
                    return ExecutionResult(
                        verdict=Verdict.TIME_LIMIT_EXCEEDED,
                        runtime=execution_time
                    )
                
                if run_result["memory_exceeded"]:
                    return ExecutionResult(
                        verdict=Verdict.MEMORY_LIMIT_EXCEEDED,
                        memory=float(memory_limit)
                    )
                
                if run_result["status_code"] != 0:
                    return ExecutionResult(
                        verdict=Verdict.RUNTIME_ERROR,
                        error=run_result["error"],
                        runtime=execution_time
                    )
                
                # Success
                return ExecutionResult(
                    verdict=Verdict.ACCEPTED,
                    output=run_result["output"].strip(),
                    runtime=execution_time,
                    memory=run_result["memory"]
                )
                
            except Exception as e:
                return ExecutionResult(
                    verdict=Verdict.RUNTIME_ERROR,
                    error=str(e)
                )
    
    async def _run_container(
        self,
        image: str,
        command: str,
        volumes: Dict,
        working_dir: str,
        timeout: int,
        memory_limit: str
    ) -> Dict:
        """Run Docker container with security constraints"""
        
        def run_docker():
            try:
                container = self.client.containers.run(
                    image=image,
                    command=f"/bin/sh -c '{command}'",
                    volumes=volumes,
                    working_dir=working_dir,
                    network_mode="none",
                    mem_limit=memory_limit,
                    memswap_limit=memory_limit,
                    cpu_quota=50000,  # 0.5 CPU
                    pids_limit=64,
                    read_only=True,
                    detach=True,
                    remove=False
                )
                
                # Wait for container with timeout
                result = container.wait(timeout=timeout)
                
                # Get logs
                output = container.logs().decode("utf-8", errors="ignore")
                
                # Get memory stats
                stats = container.stats(stream=False)
                memory_mb = stats['memory_stats'].get('usage', 0) / (1024 * 1024)
                
                # Remove container
                container.remove(force=True)
                
                return {
                    "status_code": result["StatusCode"],
                    "output": output,
                    "error": output if result["StatusCode"] != 0 else "",
                    "timeout": False,
                    "memory_exceeded": False,
                    "memory": memory_mb
                }
                
            except docker.errors.ContainerError as e:
                return {
                    "status_code": e.exit_status,
                    "output": "",
                    "error": str(e),
                    "timeout": False,
                    "memory_exceeded": False,
                    "memory": 0
                }
            except Exception as e:
                # Handle timeout
                if "timeout" in str(e).lower():
                    return {
                        "status_code": 124,
                        "output": "",
                        "error": "Time limit exceeded",
                        "timeout": True,
                        "memory_exceeded": False,
                        "memory": 0
                    }
                return {
                    "status_code": 1,
                    "output": "",
                    "error": str(e),
                    "timeout": False,
                    "memory_exceeded": False,
                    "memory": 0
                }
        
        # Run in thread pool to not block
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, run_docker)
    
    def pull_images(self):
        """Pull all required Docker images"""
        for config in self.language_configs.values():
            print(f"Pulling {config['image']}...")
            try:
                self.client.images.pull(config["image"])
            except Exception as e:
                print(f"Failed to pull {config['image']}: {e}")


# Global executor instance
executor = DockerExecutor()
