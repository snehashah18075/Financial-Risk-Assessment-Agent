import os
import re
from pathlib import Path

class FinancialRAGEngine:
    """
    Lightweight, deterministic RAG Engine for Financial Knowledge Retrieval.
    Chunks financial domain knowledge and retrieves relevant concept explanations using TF-IDF / Cosine Similarity.
    """
    def __init__(self, knowledge_dir: str = None):
        if knowledge_dir is None:
            knowledge_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
        self.knowledge_dir = Path(knowledge_dir)
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_and_index_knowledge()

    def _load_and_index_knowledge(self):
        """Load markdown knowledge files, chunk them by concept headers, and index using TF-IDF."""
        self.chunks = []
        if not self.knowledge_dir.exists():
            return

        for filepath in self.knowledge_dir.glob("*.md"):
            try:
                content = filepath.read_text(encoding="utf-8")
                # Split content into sections by headers (## Concept:)
                sections = re.split(r'\n(?=## Concept:|\n# )', content)
                for sec in sections:
                    cleaned_sec = sec.strip()
                    if cleaned_sec:
                        self.chunks.append(cleaned_sec)
            except Exception as e:
                print(f"Error reading knowledge file {filepath}: {e}")

        if not self.chunks:
            return

        # Try building TF-IDF Vectorizer with scikit-learn
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        except Exception:
            # Vectorizer will be None; retrieve_relevant_knowledge will fallback to keyword overlap
            self.vectorizer = None

    def retrieve_relevant_knowledge(self, query: str, top_k: int = 2) -> list:
        """
        Retrieve the top_k relevant knowledge snippets for a given query.
        Returns a list of matching text chunks.
        """
        if not self.chunks:
            return ["No financial knowledge base chunks available."]

        # Method 1: TF-IDF Cosine Similarity
        if self.vectorizer is not None and self.tfidf_matrix is not None:
            try:
                from sklearn.metrics.pairwise import cosine_similarity
                query_vec = self.vectorizer.transform([query])
                scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                top_indices = scores.argsort()[::-1][:top_k]
                
                results = []
                for idx in top_indices:
                    if scores[idx] > 0.05:
                        results.append(self.chunks[idx])
                
                if results:
                    return results
            except Exception as e:
                print(f"TF-IDF search error: {e}")

        # Method 2: Keyword overlap fallback
        query_words = set(re.findall(r'\w+', query.lower())) - {"the", "a", "an", "is", "of", "and", "in", "to", "for"}
        scores = []
        for chunk in self.chunks:
            chunk_words = set(re.findall(r'\w+', chunk.lower()))
            overlap = len(query_words.intersection(chunk_words))
            scores.append(overlap)

        scored_chunks = sorted(zip(scores, self.chunks), key=lambda x: x[0], reverse=True)
        results = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
        
        return results if results else self.chunks[:top_k]

    def get_knowledge_summary_for_ratios(self, risk_categories: dict) -> str:
        """
        Convenience method to pull knowledge snippets relevant to the specific high/medium risk categories.
        """
        relevant_queries = []
        for category, risk_level in risk_categories.items():
            if risk_level in ("HIGH", "MEDIUM"):
                relevant_queries.append(f"{category} financial ratio {risk_level} risk meaning")

        if not relevant_queries:
            query = "profit margin liquidity leverage current ratio quick ratio interest coverage"
        else:
            query = " ".join(relevant_queries)

        snippets = self.retrieve_relevant_knowledge(query, top_k=3)
        return "\n\n---\n\n".join(snippets)


# Global Singleton instance for easy tool access
_rag_engine_instance = None

def get_rag_engine():
    global _rag_engine_instance
    if _rag_engine_instance is None:
        _rag_engine_instance = FinancialRAGEngine()
    return _rag_engine_instance

def query_financial_knowledge(query: str) -> str:
    """Tool function to query the RAG knowledge base."""
    engine = get_rag_engine()
    results = engine.retrieve_relevant_knowledge(query, top_k=2)
    return "\n\n".join(results)


# OpenAI tool schema definition for RAG search
TOOL_RAG_SEARCH = {
    "type": "function",
    "function": {
        "name": "query_financial_knowledge",
        "description": "Retrieves relevant financial domain knowledge from the project's local financial knowledge base using the RAG system. Use this to explain financial ratios, risk concepts, and the meaning of financial indicators.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Financial concept or question to retrieve from the knowledge base."
                }
            },
            "required": ["query"]
        }
    }
}

