import ollama

MODEL = "deepseek-coder:1.3b"

def debug_error(error):

    prompt = f"""
You are a debugging AI.

Fix this error:

{error}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]