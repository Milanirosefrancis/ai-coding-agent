import os
import shutil
import stat
from git import Repo


# Fix Windows read-only delete issue
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repo(repo_url):

    clone_dir = "temp_repo"

    # Delete old repo safely
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, onerror=remove_readonly)

    print("Cloning repository...")

    Repo.clone_from(repo_url, clone_dir)

    return clone_dir


def analyze_python_repo(repo_path):

    python_files = []
    total_lines = 0
    folders = set()

    for root, dirs, files in os.walk(repo_path):

        for file in files:
            if file.endswith(".py"):

                path = os.path.join(root, file)
                python_files.append(path)

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        total_lines += len(f.readlines())
                except:
                    pass

        for d in dirs:
            folders.add(d)

    summary = f"""
Repository Analysis

Python files: {len(python_files)}
Total lines of code: {total_lines}

Folders detected:
{list(folders)}

Sample Python files:
{python_files[:10]}
"""

    return summary


def analyze_github_python(repo_url):

    repo_path = clone_repo(repo_url)

    result = analyze_python_repo(repo_path)

    return result