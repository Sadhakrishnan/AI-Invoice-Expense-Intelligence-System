from typing import Dict, Any
from .regex_extractor import extract_fields_with_regex

def extract_fields_with_llm(text: str) -> Dict[str, Any]:
    """
    Extract fields using an LLM.
    For this baseline, we will fallback to regex as no API key is provided.
    In a real scenario, this would call OpenAI API or a local LLM.
    """
    # Mock LLM usage by delegating to regex
    print("Using Regex fallback for LLM Extractor (no LLM configured).")
    return extract_fields_with_regex(text)
