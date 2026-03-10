import ollama

MODEL = "deepseek-coder:1.3b"

def generate_code(task):

    prompt = f"""
You are a coding AI.

Write code to complete this task:

{task}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]