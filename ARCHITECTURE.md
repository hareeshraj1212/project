# EduGenie Architecture

Browser → FastAPI → feature module → Gemini API

The five user-facing tasks map to these endpoints:

- `/qa` → `qna.py`
- `/explain` → `explanation_module.py`
- `/quiz` → `quiz_module.py`
- `/summarize` → `summary_module.py`
- `/learn/recommendations` → `learning_path.py`

`gemini_client.py` is the single integration layer for authentication, model selection and content generation. This prevents each feature module from duplicating SDK setup.

Quiz generation uses Pydantic structured output validation so the backend expects exactly three questions, four options per question, and a correct answer that matches one of the options.
