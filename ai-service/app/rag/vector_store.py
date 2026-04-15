import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import httpx
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class VectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.client = chromadb.PersistentClient(
            path=settings.CHROMADB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="dsa_questions",
            metadata={"hnsw:space": "cosine"}
        )
        self.ollama_url = f"{settings.OLLAMA_BASE_URL}/api/embeddings"
        self.embed_model = "nomic-embed-text:latest"
        self._initialized = True
        logger.info("VectorStore initialized with Ollama embeddings")

    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from Ollama nomic-embed-text."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.ollama_url,
                    json={"model": self.embed_model, "prompt": text}
                )
                response.raise_for_status()
                data = response.json()
                return data.get("embedding", [])
        except Exception as e:
            logger.error(f"Failed to get embedding: {e}")
            # Fallback to empty embedding (will cause issues but won't crash)
            return [0.0] * 768

    async def add_question(
        self,
        question_id: str,
        title: str,
        description: str,
        topic: str,
        difficulty: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a question to the vector store."""
        document = f"{title}\n{description}\nTopic: {topic}\nDifficulty: {difficulty}"
        embedding = await self._get_embedding(document)

        combined_metadata = {
            "question_id": question_id,
            "title": title,
            "topic": topic,
            "difficulty": difficulty,
            **(metadata or {})
        }

        self.collection.add(
            ids=[question_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[combined_metadata]
        )
        logger.info(f"Added question {question_id} to vector store")

    async def retrieve_similar_questions(
        self,
        topic: str,
        difficulty: str,
        n_results: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieve similar questions based on topic and difficulty."""
        query = f"Generate a {difficulty} difficulty DSA question about {topic}"
        query_embedding = await self._get_embedding(query)

        count = self.collection.count()
        if count == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
            where={"topic": topic}
        )

        similar_questions = []
        if results['ids'] and results['ids'][0]:
            for i, qid in enumerate(results['ids'][0]):
                similar_questions.append({
                    "question_id": qid,
                    "title": results['metadatas'][0][i].get('title', ''),
                    "topic": results['metadatas'][0][i].get('topic', ''),
                    "difficulty": results['metadatas'][0][i].get('difficulty', ''),
                    "distance": results['distances'][0][i] if results['distances'] else None,
                    "content": results['documents'][0][i] if results['documents'] else ''
                })

        return similar_questions

    def delete_question(self, question_id: str) -> None:
        """Delete a question from the vector store."""
        try:
            self.collection.delete(ids=[question_id])
            logger.info(f"Deleted question {question_id} from vector store")
        except Exception as e:
            logger.error(f"Failed to delete question {question_id}: {e}")


vector_store = VectorStore()
