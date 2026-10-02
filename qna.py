from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""You are EduGenie, an academic question-answering assistant.
Answer the student's question accurately and concisely.

Question: {question}

Requirements:
- Give the direct answer first.
- Then explain the reasoning or key context in simple language.
- If the question is ambiguous, state the assumption you are making.
- Do not invent citations, sources, statistics, or facts.
- If you are uncertain, say what is uncertain.
"""
    return generate_text(prompt, temperature=0.25, max_output_tokens=900)
