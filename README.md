# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Question answering
- Beginner-friendly concept explanations
- Three-question MCQ generation
- Educational passage summarization
- Personalized six-week learning paths

The supplied specification describes FastAPI, HTML/CSS, Gemini for Q&A/quiz/summary/learning paths, and LaMini-Flan-T5 for concept explanations. This implementation preserves those functional modules while using Google's current `google-genai` Python SDK. The Gemini model is configurable through `.env` rather than hard-coded to the older Gemini 1.5 Pro name.

## Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── local_explainer.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## VS Code setup — Ubuntu/Linux

Open the project folder in VS Code, then open **Terminal → New Terminal**.

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Upgrade pip and install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

with your Gemini API key. Do **not** commit `.env` to GitHub.

### 4. Start the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is also available at:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run the local tests:

```bash
pip install pytest
pytest -q
```

The included tests check that the application starts, the health endpoint works, and request validation rejects invalid input. They do not consume Gemini API quota.

For a live AI test, use the browser UI or `/docs` after configuring `GEMINI_API_KEY`.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"What is supervised learning?"}'
```

### Explanation

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"text":"Explain the Pythagoras theorem."}'
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"Photosynthesis is the process by which green plants use light energy to convert carbon dioxide and water into glucose and oxygen."}'
```

### Summary

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Paste an educational passage here."}'
```

### Learning path

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d '{"topic":"SQL","level":"beginner","hours_per_week":5}'
```

## Optional local LaMini explanation model

The source documentation specifies `MBZUAI/LaMini-Flan-T5-783M` for concept explanation. Because this is a large local model and is not needed for the default cloud workflow, the project keeps it optional.

Install its dependencies:

```bash
pip install "transformers>=4.45,<6.0" "torch>=2.2,<3.0"
```

Then set this in `.env`:

```text
USE_LOCAL_EXPLAINER=true
```

The first explanation request will download the model. CPU inference can be slow and memory-heavy. If the local model cannot load, EduGenie automatically falls back to Gemini.

## Troubleshooting

**`GEMINI_API_KEY is not configured`**

Make sure `.env` exists in the project root and contains a valid key, then restart Uvicorn.

**Gemini model not available**

Change `GEMINI_MODEL` in `.env` to a model currently available to your Gemini API account.

**Port 8000 is already in use**

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.
