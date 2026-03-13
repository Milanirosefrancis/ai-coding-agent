def generate_project_structure(project_name):

    return {
        "tasks":[

            {
                "tool":"create_folder",
                "args":{"path": project_name}
            },

            {
                "tool":"create_folder",
                "args":{"path": f"{project_name}/templates"}
            },

            {
                "tool":"create_folder",
                "args":{"path": f"{project_name}/static"}
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/app.py",
                    "content": """
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
"""
                }
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/templates/index.html",
                    "content": """
<!DOCTYPE html>
<html>
<head>
<title>AI Generated App</title>
</head>
<body>
<h1>Hello from your AI Built App</h1>
</body>
</html>
"""
                }
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/requirements.txt",
                    "content": "flask"
                }
            }

        ]
    }