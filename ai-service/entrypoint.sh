#!/bin/bash
set -e

echo "Waiting for Ollama to be ready..."
until curl -f http://ollama:11434/api/tags > /dev/null 2>&1; do
    echo "Ollama not ready yet, waiting..."
    sleep 5
done

echo "Ollama is ready. Pulling required models..."

# Pull embedding model
echo "Pulling nomic-embed-text:latest..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "nomic-embed-text:latest"}' > /dev/null 2>&1 &

# Pull LLM model
echo "Pulling llama3.1:8b..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "llama3.1:8b"}' > /dev/null 2>&1 &

# Wait for pulls to complete
wait
echo "Models pulled successfully!"

echo "Starting AI service..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
