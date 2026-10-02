from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner", hours_per_week: int = 5) -> str:
    prompt = f"""Create a practical learning path for: {topic}
Current level: {level}
Available time: {hours_per_week} hours/week

Structure the answer as:
1. Goal
2. Week-by-week plan for 6 weeks
3. Beginner -> intermediate -> advanced concepts
4. A small project for practice
5. Recommended resource types (official docs, tutorials, videos, books)
6. A weekly self-check method

Do not invent specific URLs. Keep the plan realistic for a student.
"""
    return generate_text(prompt, temperature=0.45, max_output_tokens=1800)
