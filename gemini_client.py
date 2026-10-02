import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not API_KEY:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Google Gemini API key."
        )
    return genai.Client(api_key=API_KEY)


def generate_text(prompt: str, *, temperature: float = 0.4, max_output_tokens: int = 1200) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def generate_json(prompt: str, response_schema, *, temperature: float = 0.3, max_output_tokens: int = 1800):
    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return response.text
