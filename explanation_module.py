import os

from gemini_client import generate_text


def explain_concept(concept: str) -> str:
    """Explain a concept at beginner level. Gemini is the default implementation.

    The original project documentation names LaMini-Flan-T5 as the local explanation model.
    Set USE_LOCAL_EXPLAINER=true to attempt that optional implementation.
    """
    if os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true":
        try:
            from local_explainer import explain_with_lamini
            return explain_with_lamini(concept)
        except Exception:
            # Keep the application usable if the optional local model is unavailable.
            pass

    prompt = f"""You are EduGenie, a patient educational tutor.
Explain the following concept for a beginner.

Concept: {concept}

Rules:
- Start with a one-sentence definition.
- Use simple language.
- Give one intuitive example or analogy.
- Use short bullets where useful.
- Avoid unnecessary jargon.
- End with one quick check question.
"""
    return generate_text(prompt, temperature=0.35, max_output_tokens=700)
