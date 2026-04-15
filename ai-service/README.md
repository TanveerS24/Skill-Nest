# AI RAG DSA Engine

A production-ready Python FastAPI microservice that acts as a RAG-based AI engine for generating DSA coding questions and executing user-submitted code.

## Architecture

- **Main Backend**: Spring Boot (existing)
- **AI Microservice**: This FastAPI service
- **Communication**: REST API (JSON)
- **LLM**: Ollama (local, http://localhost:11434)
- **Vector Store**: ChromaDB
- **Database**: PostgreSQL
- **Cache**: Redis

## Features

1. **RAG-Based DSA Question Generation**: Generate unique coding problems using vector similarity search + LLM
2. **Vector Store**: ChromaDB for storing and retrieving similar questions
3. **Code Execution Engine**: Support for Python, Java, and C++ with safety controls
4. **Redis Caching**: Cache generated questions and temporary results
5. **PostgreSQL Storage**: Persistent storage for questions, test cases, and submissions

## Project Structure

```
app/
 ├── main.py              # FastAPI application entry point
 ├── core/                # Configuration and logging
 │   ├── config.py
 │   └── logging.py
 ├── db/                  # Database models and connection
 │   ├── base.py
 │   ├── models.py
 │   └── init_db.py
 ├── schemas/             # Pydantic schemas
 │   └── schemas.py
 ├── routes/              # API endpoints
 │   ├── health.py
 │   ├── questions.py
 │   └── execution.py
 ├── services/            # Business logic
 │   └── question_service.py
 ├── rag/                 # RAG components
 │   ├── vector_store.py
 │   └── ollama_client.py
 ├── execution/           # Code execution
 │   └── code_executor.py
 └── utils/               # Utilities
     └── cache.py
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- Ollama (with llama3 model)

### Local Development

1. **Create virtual environment and install dependencies**:
```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Ensure Ollama is running**:
```bash
ollama run llama3
```

4. **Start PostgreSQL and Redis** (if using Docker):
```bash
docker-compose up -d postgres redis
```

5. **Run the application**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

```bash
docker-compose up -d
```

## API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "redis": "connected"
}
```

### Generate Question
```bash
POST /questions/generate
Content-Type: application/json

{
  "topic": "graphs",
  "difficulty": "medium"
}
```

Response:
```json
{
  "question_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Find the Shortest Path",
  "description": "Given a weighted undirected graph...",
  "constraints": "1 <= n <= 1000",
  "examples": [
    {"input": "4 4\n1 2 1\n2 3 2\n3 4 1\n1 4 5", "output": "3"}
  ],
  "test_cases": [
    {"input": "...", "output": "..."}
  ],
  "starter_code": {
    "java": "class Solution { public int shortestPath(int n, int[][] edges) { } }",
    "python": "def shortest_path(n, edges):",
    "cpp": "class Solution { public: int shortestPath(int n, vector<vector<int>>& edges) { } };"
  }
}
```

### List Questions
```bash
GET /questions?topic=graphs&difficulty=medium&limit=10&offset=0
```

### Get Question by ID
```bash
GET /questions/{question_id}
```

### Run Code (Preview)
```bash
POST /execute/run
Content-Type: application/json

{
  "question_id": "550e8400-e29b-41d4-a716-446655440000",
  "language": "python",
  "code": "def solution(n, edges): return 3"
}
```

Response:
```json
{
  "status": "accepted",
  "results": [
    {
      "input": "4 4\n1 2 1",
      "expected": "3",
      "actual": "3",
      "passed": true
    }
  ],
  "execution_time_ms": 45.2,
  "stderr": null
}
```

### Submit Code
```bash
POST /execute/submit
Content-Type: application/json

{
  "question_id": "550e8400-e29b-41d4-a716-446655440000",
  "language": "java",
  "code": "class Solution { public int shortestPath(int n, int[][] edges) { return 3; } }"
}
```

Same response format as `/run`, but stores the submission in the database.

## Integration with Spring Boot

Example Spring Boot REST client configuration:

```java
@Configuration
public class AIServiceConfig {
    
    @Bean
    public WebClient aiServiceWebClient() {
        return WebClient.builder()
            .baseUrl("http://localhost:8000")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();
    }
}

@Service
public class QuestionService {
    
    @Autowired
    private WebClient aiServiceWebClient;
    
    public Mono<GeneratedQuestion> generateQuestion(String topic, String difficulty) {
        return aiServiceWebClient.post()
            .uri("/questions/generate")
            .bodyValue(Map.of("topic", topic, "difficulty", difficulty))
            .retrieve()
            .bodyToMono(GeneratedQuestion.class);
    }
    
    public Mono<ExecutionResult> submitCode(String questionId, String language, String code) {
        return aiServiceWebClient.post()
            .uri("/execute/submit")
            .bodyValue(Map.of(
                "question_id", questionId,
                "language", language,
                "code", code
            ))
            .retrieve()
            .bodyToMono(ExecutionResult.class);
    }
}
```

## Example curl Requests

### Generate a Question
```bash
curl -X POST http://localhost:8000/questions/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "arrays",
    "difficulty": "easy"
  }'
```

### Run Python Code
```bash
curl -X POST http://localhost:8000/execute/run \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "YOUR_QUESTION_ID",
    "language": "python",
    "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []"
  }'
```

### Run Java Code
```bash
curl -X POST http://localhost:8000/execute/run \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "YOUR_QUESTION_ID",
    "language": "java",
    "code": "import java.util.*;\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        Map<Integer, Integer> map = new HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int complement = target - nums[i];\n            if (map.containsKey(complement)) {\n                return new int[] { map.get(complement), i };\n            }\n            map.put(nums[i], i);\n        }\n        return new int[] {};\n    }\n}"
  }'
```

### Run C++ Code
```bash
curl -X POST http://localhost:8000/execute/run \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "YOUR_QUESTION_ID",
    "language": "cpp",
    "code": "#include <vector>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        unordered_map<int, int> map;\n        for (int i = 0; i < nums.size(); i++) {\n            int complement = target - nums[i];\n            if (map.find(complement) != map.end()) {\n                return {map[complement], i};\n            }\n            map[nums[i]] = i;\n        }\n        return {};\n    }\n};"
  }'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection URL | postgresql://postgres:postgres@localhost:5432/ai_service |
| REDIS_HOST | Redis host | localhost |
| REDIS_PORT | Redis port | 6379 |
| OLLAMA_BASE_URL | Ollama API URL | http://localhost:11434 |
| OLLAMA_MODEL | Ollama model name | llama3 |
| CHROMADB_PATH | ChromaDB storage path | ./chroma_db |
| EXECUTION_TIMEOUT | Code execution timeout (seconds) | 2 |
| DEBUG | Enable debug mode | false |

## Security Notes

- Code execution uses subprocess with timeout and memory limits
- Temporary files are cleaned up after execution
- Resource limits are enforced on Unix systems
- No network access is granted to submitted code

## License

MIT
