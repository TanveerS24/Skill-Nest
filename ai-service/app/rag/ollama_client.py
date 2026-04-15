import httpx
import json
import re
from typing import Dict, Any, List, Optional
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 120.0

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using Ollama API."""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            raise Exception("LLM generation timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"LLM service error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")

    async def generate_dsa_question(
        self,
        topic: str,
        difficulty: str,
        similar_questions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a DSA question using RAG context."""

        context = ""
        if similar_questions:
            context = "Here are some similar questions for reference:\n\n"
            for i, q in enumerate(similar_questions[:3], 1):
                context += f"{i}. {q['title']} ({q['difficulty']})\n"
                if q.get('content'):
                    content_preview = q['content'][:200] + "..." if len(q['content']) > 200 else q['content']
                    context += f"   Preview: {content_preview}\n"
            context += "\nUse these as inspiration but create a NEW, UNIQUE question.\n\n"

        system_prompt = """You are an expert DSA (Data Structures and Algorithms) instructor. 
Generate high-quality coding interview questions in valid JSON format only.

Rules:
1. Output must be ONLY valid JSON, no markdown formatting, no extra text
2. Include exactly 10 test cases
3. First 2 test cases should be simple examples suitable for problem description
4. Provide starter code templates for Java, Python, and C++
5. Make sure the question is solvable and test cases are correct
6. Constraints should be realistic

JSON Structure:
{
    "title": "string",
    "description": "string with problem statement",
    "constraints": "string with constraints",
    "examples": [{"input": "...", "output": "...", "explanation": "..."}],
    "test_cases": [{"input": "...", "output": "..."}],
    "starter_code": {
        "java": "class Solution { ... }",
        "python": "def solution(...): ...",
        "cpp": "class Solution { public: ... }"
    }
}"""

        user_prompt = f"""{context}Generate a {difficulty.upper()} difficulty DSA question about {topic.upper()}.

Requirements:
- Topic: {topic}
- Difficulty: {difficulty}
- Must include exactly 10 test cases
- Problem should be clear, well-defined, and suitable for a 45-minute interview
- Test cases should cover edge cases, normal cases, and boundary conditions

Generate the complete question now:"""

        response_text = await self.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.8,
            max_tokens=4000
        )

        # Extract JSON from response
        try:
            # Try to find JSON in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON between curly braces
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = response_text

            question_data = json.loads(json_str)

            # Validate required fields
            required_fields = ["title", "description", "test_cases", "starter_code"]
            for field in required_fields:
                if field not in question_data:
                    raise ValueError(f"Missing required field: {field}")

            # Ensure exactly 10 test cases
            test_cases = question_data.get("test_cases", [])
            if len(test_cases) < 10:
                logger.warning(f"Only {len(test_cases)} test cases provided, expected 10")
                # Pad with generic test cases if needed
                while len(test_cases) < 10:
                    test_cases.append({
                        "input": test_cases[-1]["input"] if test_cases else "",
                        "output": test_cases[-1]["output"] if test_cases else ""
                    })
                question_data["test_cases"] = test_cases[:10]
            elif len(test_cases) > 10:
                question_data["test_cases"] = test_cases[:10]

            return question_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response: {response_text[:500]}...")
            raise Exception(f"Failed to generate valid question format: {e}")


ollama_client = OllamaClient()
