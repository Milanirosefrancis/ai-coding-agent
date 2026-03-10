import ollama

MODEL = "deepseek-coder:1.3b"

def create_plan(task):

    prompt = f"""
You are a planning AI.

Break the following task into steps.

Task:
{task}

Return steps as a list.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]