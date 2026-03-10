import os
import subprocess


# -----------------------------
# List all files in the project
# -----------------------------
def list_files():
    files = []
    for root, dirs, filenames in os.walk("."):
        for name in filenames:
            files.append(os.path.join(root, name))
    return files


# -----------------------------
# Read a file
# -----------------------------
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


# -----------------------------
# Write or update a file
# -----------------------------
def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return "File written successfully"
    except Exception as e:
        return f"Error writing file: {str(e)}"


# -----------------------------
# Run a Python file
# -----------------------------
def run_python(file):
    try:
        result = subprocess.run(
            ["python", file],
            capture_output=True,
            text=True
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running python file: {str(e)}"