from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational passage below for quick revision.
Keep the important facts and relationships, remove repetition, and use clear language.
Return a concise heading followed by 4-8 bullet points.

PASSAGE:
{text}
"""
    return generate_text(prompt, temperature=0.25, max_output_tokens=900)
