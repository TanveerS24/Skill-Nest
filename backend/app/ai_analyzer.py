import httpx
import json
from typing import List
from app.config import get_settings
from app.schemas import AIAnalysisResult
from app.models import Language, Verdict

settings = get_settings()


class AICodeAnalyzer:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.api_url = settings.AI_API_URL
    
    async def analyze_code(self, code: str, language: Language) -> AIAnalysisResult:
        """
        Analyze code for security issues and complexity estimation
        """
        # Basic pattern matching for unsafe code
        is_safe, issues = self._check_unsafe_patterns(code, language)
        
        if not is_safe:
            return AIAnalysisResult(
                is_safe=False,
                issues=issues
            )
        
        # If AI API is configured, use it for complexity analysis
        if self.api_key:
            try:
                complexity_result = await self._ai_complexity_analysis(code, language)
                return AIAnalysisResult(
                    is_safe=True,
                    time_complexity=complexity_result.get("time_complexity"),
                    space_complexity=complexity_result.get("space_complexity"),
                    issues=[]
                )
            except Exception as e:
                # Fallback to basic analysis if AI fails
                print(f"AI analysis failed: {e}")
                return self._fallback_analysis()
        else:
            # Use fallback analysis
            return self._fallback_analysis()
    
    def _check_unsafe_patterns(self, code: str, language: Language) -> tuple[bool, List[str]]:
        """Check for dangerous patterns in code"""
        issues = []
        
        # Common dangerous patterns across languages
        dangerous_patterns = {
            "system": ["system(", "exec(", "eval(", "subprocess", "os.system"],
            "file_ops": ["open(", "file(", "fopen", "read(", "write("],
            "network": ["socket", "urllib", "requests", "httpx", "curl"],
            "import": ["import os", "import sys", "import subprocess", "__import__"],
            "fork_bomb": ["fork(", "while True", "while(1)", "for(;;)"],
        }
        
        code_lower = code.lower()
        
        for category, patterns in dangerous_patterns.items():
            for pattern in patterns:
                if pattern.lower() in code_lower:
                    issues.append(f"Potentially unsafe pattern detected: {pattern}")
        
        # Check for very long loops (potential infinite loops)
        if "while" in code_lower and "break" not in code_lower:
            issues.append("Potential infinite loop detected (while without break)")
        
        return len(issues) == 0, issues
    
    async def _ai_complexity_analysis(self, code: str, language: Language) -> dict:
        """Use AI API to estimate time and space complexity"""
        prompt = f"""Analyze the following {language.value} code and provide:
1. Time complexity (in Big O notation)
2. Space complexity (in Big O notation)

Code:
```{language.value}
{code}
```

Respond in JSON format:
{{
    "time_complexity": "O(...)",
    "space_complexity": "O(...)"
}}
"""
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a code analysis expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Try to parse JSON from response
                try:
                    # Extract JSON from markdown code blocks if present
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                    
                    complexity_data = json.loads(content)
                    return complexity_data
                except json.JSONDecodeError:
                    # Fallback parsing
                    return {
                        "time_complexity": "O(n)",
                        "space_complexity": "O(1)"
                    }
            else:
                raise Exception(f"AI API error: {response.status_code}")
    
    def _fallback_analysis(self) -> AIAnalysisResult:
        """Fallback analysis when AI is not available"""
        return AIAnalysisResult(
            is_safe=True,
            time_complexity="O(n)",
            space_complexity="O(1)",
            issues=[]
        )


# Global analyzer instance
analyzer = AICodeAnalyzer()
