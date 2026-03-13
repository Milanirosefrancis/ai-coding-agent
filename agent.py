import ollama
import json
import re

from supabase_memory import get_memory, add_memory
from tools.file_tools import list_files, read_file, write_file, run_python, create_folder
from tools.universal_link_analyzer import analyze_link
from vector_memory import store_memory, search_memory

# Multi-Agent imports
from core.planner_agent import create_plan
from core.coder_agent import generate_flask_project
from core.project_planner import generate_project_structure
from core.debugger_agent import debug_error

from tools.github_analyzer import analyze_github_repo
from tools.web_analyzer import analyze_webpage

from state_manager import AgentState


MODEL = "llama3"

state = AgentState()


# -----------------------------
# TOOL EXECUTION
# -----------------------------
def execute_tool(tool, args):

    print("Executing tool:", tool)

    if tool == "list_files":
        result = list_files()

    elif tool == "read_file":
        result = read_file(args.get("path"))

    elif tool == "write_file":
        result = write_file(
            args.get("path"),
            args.get("content")
        )

    elif tool == "create_folder":
        result = create_folder(args.get("path"))

    elif tool == "run_python":
        result = run_python(args.get("file"))

    elif tool == "analyze_github":
        result = analyze_github_repo(args.get("url"))

    elif tool == "analyze_web":
        result = analyze_webpage(args.get("url"))
    elif tool == "analyze_link":
        result = analyze_link(args.get("url"))

    else:
        result = "Unknown tool"

    print("Tool result:", result)

    return result


# -----------------------------
# MULTI TASK EXECUTOR
# -----------------------------
def execute_task_list(tasks):

    results = []

    for task in tasks:

        tool = task.get("tool")
        args = task.get("args", {})

        print("\nExecuting task:", tool)

        result = execute_tool(tool, args)

        results.append(result)

    return results


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def extract_json(text):

    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except:
        return None


# -----------------------------
# LINK DETECTOR
# -----------------------------
def detect_link(text):

    urls = re.findall(r'https?://[^\s]+', text)

    if not urls:
        return None

    url = urls[0]

    if "github.com" in url:
        return {"tool": "analyze_github", "args": {"url": url}}

    return {"tool": "analyze_link", "args": {"url": url}}


# -----------------------------
# AUTONOMOUS LOOP
# -----------------------------
def autonomous_loop(task, max_steps=6):

    current_task = task

    for step in range(max_steps):

        print(f"\n----- AGENT STEP {step+1} -----")

        response = ask_agent(current_task)

        print("Agent:", response)

        if "task complete" in str(response).lower():
            break

        current_task = str(response)

    return "Task finished"


# -----------------------------
# MAIN AGENT
# -----------------------------
def ask_agent(prompt):

    state.set_task(prompt)

    # -----------------------------
    # CHECK IF USER SENT A LINK
    # -----------------------------
    link_tool = detect_link(prompt)

    if link_tool:
        print("Detected URL. Running analyzer tool...")

        result = execute_tool(
            link_tool["tool"],
            link_tool["args"]
        )

        summary_prompt = f"""
Summarize the following project or webpage.

Explain:
- What it is
- What it does
- Technologies used
- Key features

Content:
{result}
"""

        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": summary_prompt}]
        )

        summary = response["message"]["content"]

        print("\nProject Summary:\n", summary)

        return summary

    # -----------------------------
    # VECTOR MEMORY
    # -----------------------------
    store_memory(prompt)
    related_memory = search_memory(prompt)

    # -----------------------------
    # PLANNER AGENT
    # -----------------------------
    plan = create_plan(prompt)
    state.add_step(plan)

    # -----------------------------
    # SYSTEM PROMPT
    # -----------------------------
    system_prompt = f"""
You are an autonomous AI coding agent.

You can:
- Plan tasks
- Write code
- Debug code
- Use tools

TOOLS AVAILABLE:

1. list_files()
2. read_file(path)
3. write_file(path, content)
4. run_python(file)
5. create_folder(path)
6. analyze_github(url)
7. analyze_web(url)
8. analyze_link(url)

You may execute a single tool OR multiple tasks.

Single tool format:

{{
 "tool": "write_file",
 "args": {{
   "path": "hello.py",
   "content": "print('Hello World')"
 }}
}}

Multi-task format:

{{
 "tasks":[
   {{"tool":"create_folder","args":{{"path":"project"}}}},
   {{"tool":"write_file","args":{{"path":"project/app.py","content":"print('hello')"}}}}
 ]
}}

Respond ONLY with JSON if using tools.

Relevant memory:
{related_memory}

Current plan:
{plan}
"""

    add_memory("user", prompt)

    messages = get_memory()
    messages = messages[-6:]

    messages.insert(0, {
        "role": "system",
        "content": system_prompt
    })

    # -----------------------------
    # CALL MODEL
    # -----------------------------
    print("Calling Ollama model...")

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    print("Model responded")

    answer = response["message"]["content"]

    print("\nModel Output:\n", answer)

    # -----------------------------
    # AUTONOMOUS PROJECT BUILDER
    # -----------------------------
    if "build project" in prompt.lower():

        project_name = "ai_generated_app"

        print("Generating full project structure...")

        project_tasks = generate_project_structure(project_name)

        results = execute_task_list(project_tasks["tasks"])

        return results

    # -----------------------------
    # FLASK PROJECT GENERATION
    # -----------------------------
    if "flask api" in prompt.lower() or "flask project" in prompt.lower():

        project_name = "flask_api"

        tasks = generate_flask_project(project_name)

        print("Generating Flask project...")

        results = execute_task_list(tasks["tasks"])

        return results

    # -----------------------------
    # TOOL EXECUTION
    # -----------------------------
    tool_data = extract_json(answer)

    if tool_data:

        if "tasks" in tool_data:

            print("Executing multiple tasks...")

            results = execute_task_list(tool_data["tasks"])

            add_memory("assistant", str(results))

            return results

        tool = tool_data.get("tool")
        args = tool_data.get("args", {})

        result = execute_tool(tool, args)

        add_memory("assistant", str(result))

        state.add_history({
            "tool": tool,
            "result": result
        })

        return result

    # -----------------------------
    # DEBUGGER AGENT
    # -----------------------------
    if "error" in answer.lower() or "traceback" in answer.lower():

        debug_result = debug_error(answer)

        add_memory("assistant", debug_result)

        return debug_result

    # -----------------------------
    # AUTO CODE DETECTION
    # -----------------------------
    if "```python" in answer:

        try:

            print("Python code detected")

            code = answer.split("```python")[1].split("```")[0]

            filename = "generated_code.py"

            write_file(filename, code)

            print("File created:", filename)

            result = run_python(filename)

            print("Execution Result:", result)

            add_memory("assistant", str(result))

            return result

        except Exception as e:
            print("Code execution failed:", e)

    # -----------------------------
    # NORMAL RESPONSE
    # -----------------------------
    add_memory("assistant", answer)

    state.add_history(answer)

    return answer