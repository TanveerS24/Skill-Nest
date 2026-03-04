import chromadb
from chromadb.config import Settings as ChromaSettings
import ollama
from typing import Optional, Dict
from app.config import settings


class RAGService:
    """RAG-based language detection using Ollama and ChromaDB"""
    
    # Language documentation snippets for embedding
    LANGUAGE_DOCS = {
        "python": """
        Python is a high-level, interpreted programming language.
        Common patterns: def, class, import, if __name__ == '__main__':
        Syntax: indentation-based, uses colons, print() function
        Example: def hello(): print("Hello World")
        """,
        "cpp": """
        C++ is a compiled, statically-typed programming language.
        Common patterns: #include, int main(), std::, using namespace
        Syntax: semicolons, curly braces, cout, cin
        Example: int main() { std::cout << "Hello"; return 0; }
        """,
        "java": """
        Java is a compiled, object-oriented programming language.
        Common patterns: public class, public static void main, System.out.println
        Syntax: strict typing, curly braces, semicolons
        Example: public class Main { public static void main(String[] args) {} }
        """,
        "javascript": """
        JavaScript is an interpreted, dynamically-typed language.
        Common patterns: function, const, let, var, console.log, =>
        Syntax: curly braces, semicolons optional, async/await
        Example: function hello() { console.log("Hello"); }
        """,
    }
    
    def __init__(self):
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIR,
                anonymized_telemetry=False,
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection("language_docs")
        except:
            self.collection = self.chroma_client.create_collection(
                name="language_docs",
                metadata={"description": "Programming language documentation"},
            )
            self._populate_collection()
    
    def _populate_collection(self):
        """Populate ChromaDB with language documentation"""
        for lang, doc in self.LANGUAGE_DOCS.items():
            # Generate embedding using Ollama
            try:
                response = ollama.embeddings(
                    model=settings.EMBED_MODEL,
                    prompt=doc,
                )
                embedding = response["embedding"]
                
                # Add to collection
                self.collection.add(
                    embeddings=[embedding],
                    documents=[doc],
                    ids=[lang],
                    metadatas=[{"language": lang}],
                )
            except Exception as e:
                print(f"Warning: Could not embed {lang} docs: {e}")
    
    async def detect_language(self, code: str) -> Dict[str, any]:
        """
        Detect programming language using RAG.
        Returns: {"language": str, "confidence": float}
        """
        try:
            # Generate embedding for the code
            response = ollama.embeddings(
                model=settings.EMBED_MODEL,
                prompt=code[:1000],  # Use first 1000 chars
            )
            code_embedding = response["embedding"]
            
            # Query similar documents
            results = self.collection.query(
                query_embeddings=[code_embedding],
                n_results=3,
            )
            
            if not results["ids"] or not results["ids"][0]:
                return {"language": "unknown", "confidence": 0.0}
            
            # Get top match
            top_languages = results["ids"][0]
            top_distances = results["distances"][0]
            
            # Build context from retrieved docs
            context = "\n\n".join(
                [f"Language: {lang}\n{doc}" 
                 for lang, doc in zip(results["ids"][0], results["documents"][0])]
            )
            
            # Ask LLM to classify with context
            prompt = f"""Based on the following language documentation:

{context}

Analyze this code and identify which programming language it is:

```
{code[:500]}
```

Respond with ONLY the language name (python, cpp, java, or javascript). 
If you're not sure, respond with your best guess."""
            
            llm_response = ollama.generate(
                model=settings.OLLAMA_MODEL,
                prompt=prompt,
            )
            
            detected = llm_response["response"].strip().lower()
            
            # Clean up response
            for lang in ["python", "cpp", "java", "javascript"]:
                if lang in detected:
                    # Calculate confidence based on distance
                    confidence = max(0.0, 1.0 - top_distances[0])
                    return {"language": lang, "confidence": round(confidence, 2)}
            
            return {"language": "unknown", "confidence": 0.0}
        
        except Exception as e:
            print(f"RAG detection error: {e}")
            # Fallback to simple heuristics
            return self._fallback_detection(code)
    
    def _fallback_detection(self, code: str) -> Dict[str, any]:
        """Simple heuristic-based fallback detection"""
        code_lower = code.lower()
        
        if "def " in code_lower or "import " in code_lower:
            return {"language": "python", "confidence": 0.6}
        elif "public class" in code_lower or "public static void main" in code_lower:
            return {"language": "java", "confidence": 0.6}
        elif "#include" in code_lower or "std::" in code_lower:
            return {"language": "cpp", "confidence": 0.6}
        elif "function" in code_lower or "console.log" in code_lower or "const " in code_lower:
            return {"language": "javascript", "confidence": 0.6}
        
        return {"language": "unknown", "confidence": 0.0}
