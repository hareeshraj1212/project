from functools import lru_cache

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"


@lru_cache(maxsize=1)
def _pipeline():
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=-1,
    )


def explain_with_lamini(concept: str) -> str:
    prompt = (
        "Explain this educational concept simply for a beginner. "
        "Use a short definition, a simple example, and 3 key points: "
        f"{concept}"
    )
    result = _pipeline()(prompt, max_new_tokens=350, do_sample=False)
    return result[0]["generated_text"].strip()
