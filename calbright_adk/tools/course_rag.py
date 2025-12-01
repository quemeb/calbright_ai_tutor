import os
from typing import Optional, Literal, Dict, Any
from dotenv import load_dotenv

from rag_tools import RAGEngine

load_dotenv()

# Global RAG instance (FAISS + metadata)
_rag = RAGEngine()

def course_rag(
    question: str,
    module: Optional[Literal["SQL", "Sheets"]] = None,
    k: int = 5,
) -> Dict[str, Any]:
    """
    ADK tool wrapping your FAISS RAG.

    Args:
        question: Student question.
        module: Optional filter ("SQL" or "Sheets").
        k: number of chunks.

    Returns:
        dict with 'results' list of docs (metadata dicts),
        plus 'module' and 'num_results'.
    """
    try:
        docs = _rag.query(question, module_filter=module, k=k)
    except Exception as e:
        return {"error": str(e), "results": [], "module": module, "num_results": 0}

    return {
        "results": docs,
        "module": module,
        "num_results": len(docs),
    }
