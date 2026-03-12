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
def create_folder(path):
    try:
        base_dir = os.getcwd()

        # only keep folder name (ignore model paths)
        folder_name = os.path.basename(path)

        full_path = os.path.join(base_dir, folder_name)

        os.makedirs(full_path, exist_ok=True)

        return f"Folder '{folder_name}' created in project directory"

    except Exception as e:
        return f"Error creating folder: {str(e)}"