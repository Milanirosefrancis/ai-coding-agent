import os
import git
import shutil


def analyze_github_repo(repo_url):

    folder = "temp_repo"

    # remove old repo if exists
    if os.path.exists(folder):
        shutil.rmtree(folder)

    # clone repo
    git.Repo.clone_from(repo_url, folder)

    summary_data = []

    for root, dirs, files in os.walk(folder):

        for file in files:

            if file.lower() in ["readme.md", "readme.txt"]:
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    summary_data.append(f.read())

    return "\n".join(summary_data)[:5000]