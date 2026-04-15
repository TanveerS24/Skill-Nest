import subprocess
import tempfile
import os
import shutil
import signal
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: float
    timeout: bool = False


class CodeExecutor:
    def __init__(self):
        self.timeout = settings.EXECUTION_TIMEOUT
        self.max_output_size = settings.MAX_OUTPUT_SIZE
        self.work_dir = tempfile.mkdtemp(prefix="code_exec_")

    def __del__(self):
        try:
            if os.path.exists(self.work_dir):
                shutil.rmtree(self.work_dir, ignore_errors=True)
        except Exception:
            pass

    def _clean_output(self, output: str) -> str:
        """Clean and truncate output if needed."""
        if len(output) > self.max_output_size:
            output = output[:self.max_output_size] + "\n... (output truncated)"
        return output.strip()

    def _run_command(
        self,
        command: List[str],
        input_data: str = "",
        cwd: Optional[str] = None
    ) -> ExecutionResult:
        """Run a command with timeout and resource limits."""
        import time

        start_time = time.time()
        timeout_occurred = False

        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd or self.work_dir,
                preexec_fn=self._set_resource_limits if os.name != 'nt' else None
            )

            try:
                stdout, stderr = process.communicate(
                    input=input_data,
                    timeout=self.timeout
                )
            except subprocess.TimeoutExpired:
                timeout_occurred = True
                process.kill()
                try:
                    stdout, stderr = process.communicate(timeout=1)
                except:
                    stdout, stderr = "", "Execution timed out"

            execution_time_ms = (time.time() - start_time) * 1000

            return ExecutionResult(
                stdout=self._clean_output(stdout),
                stderr=self._clean_output(stderr),
                exit_code=process.returncode,
                execution_time_ms=execution_time_ms,
                timeout=timeout_occurred
            )

        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr=f"Execution error: {str(e)}",
                exit_code=-1,
                execution_time_ms=(time.time() - start_time) * 1000,
                timeout=False
            )

    def _set_resource_limits(self):
        """Set resource limits for the child process (Unix only)."""
        try:
            import resource
            # Limit memory to 256MB
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
            # Limit CPU time
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
        except Exception:
            pass

    def execute_python(self, code: str, input_data: str = "") -> ExecutionResult:
        """Execute Python code."""
        file_path = os.path.join(self.work_dir, "solution.py")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        return self._run_command(
            ["python3", "-B", "solution.py"],
            input_data=input_data
        )

    def execute_java(self, code: str, input_data: str = "") -> ExecutionResult:
        """Execute Java code."""
        # Extract class name from code
        import re
        class_match = re.search(r'class\s+(\w+)', code)
        if not class_match:
            return ExecutionResult(
                stdout="",
                stderr="Error: Could not find public class in code",
                exit_code=-1,
                execution_time_ms=0
            )

        class_name = class_match.group(1)
        java_file = os.path.join(self.work_dir, f"{class_name}.java")

        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(code)

        # Compile
        compile_result = self._run_command(["javac", java_file])
        if compile_result.exit_code != 0:
            return ExecutionResult(
                stdout="",
                stderr=f"Compilation Error:\n{compile_result.stderr}",
                exit_code=-1,
                execution_time_ms=compile_result.execution_time_ms
            )

        # Run
        return self._run_command(
            ["java", "-cp", self.work_dir, class_name],
            input_data=input_data
        )

    def execute_cpp(self, code: str, input_data: str = "") -> ExecutionResult:
        """Execute C++ code."""
        source_file = os.path.join(self.work_dir, "solution.cpp")
        binary_file = os.path.join(self.work_dir, "solution")
        if os.name == 'nt':
            binary_file += ".exe"

        with open(source_file, 'w', encoding='utf-8') as f:
            f.write(code)

        # Compile
        compile_result = self._run_command(
            ["g++", "-std=c++17", "-O2", "-o", binary_file, source_file]
        )
        if compile_result.exit_code != 0:
            return ExecutionResult(
                stdout="",
                stderr=f"Compilation Error:\n{compile_result.stderr}",
                exit_code=-1,
                execution_time_ms=compile_result.execution_time_ms
            )

        # Run
        return self._run_command([binary_file], input_data=input_data)

    def execute(
        self,
        language: str,
        code: str,
        test_cases: List[Dict[str, str]]
    ) -> Dict:
        """Execute code against multiple test cases."""
        results = []
        all_passed = True
        total_time = 0
        aggregated_stderr = []

        for i, test_case in enumerate(test_cases):
            input_data = test_case.get("input", "")
            expected_output = test_case.get("expected_output", "").strip()

            # Execute based on language
            if language.lower() in ["python", "py"]:
                result = self.execute_python(code, input_data)
            elif language.lower() == "java":
                result = self.execute_java(code, input_data)
            elif language.lower() in ["cpp", "c++", "cxx"]:
                result = self.execute_cpp(code, input_data)
            else:
                return {
                    "status": "error",
                    "error": f"Unsupported language: {language}",
                    "results": []
                }

            total_time += result.execution_time_ms

            if result.stderr:
                aggregated_stderr.append(f"Test case {i+1}: {result.stderr}")

            actual_output = result.stdout.strip()
            passed = actual_output == expected_output and result.exit_code == 0 and not result.timeout

            if not passed:
                all_passed = False

            results.append({
                "test_case_index": i,
                "input": input_data,
                "expected": expected_output,
                "actual": actual_output,
                "passed": passed,
                "timeout": result.timeout,
                "exit_code": result.exit_code,
                "execution_time_ms": result.execution_time_ms
            })

        status = "accepted" if all_passed else "wrong_answer"
        if any(r["timeout"] for r in results):
            status = "time_limit_exceeded"
        if any(r["exit_code"] != 0 for r in results if not r["timeout"]):
            status = "runtime_error"

        return {
            "status": status,
            "results": results,
            "total_execution_time_ms": total_time,
            "stderr": "\n".join(aggregated_stderr) if aggregated_stderr else None
        }
