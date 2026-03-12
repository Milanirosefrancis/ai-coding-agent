def generate_flask_project(project_name):

    return {
        "tasks":[

            {
                "tool":"create_folder",
                "args":{"path": project_name}
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/app.py",
                    "content": """
from flask import Flask
from routes import api

app = Flask(__name__)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
"""
                }
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/routes.py",
                    "content": """
from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route("/")
def home():
    return jsonify({"message":"API running"})
"""
                }
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/requirements.txt",
                    "content": "flask"
                }
            },

            {
                "tool":"write_file",
                "args":{
                    "path": f"{project_name}/README.md",
                    "content": "# Flask API Project"
                }
            }

        ]
    }