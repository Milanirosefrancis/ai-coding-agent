import ollama
import json

from supabase_memory import get_memory, add_memory
from tools import list_files, read_file, write_file, run_python
from vector_memory import store_memory, search_memory

# Multi-Agent imports
from core.planner_agent import create_plan
from core.coder_agent import generate_code
from core.debugger_agent import debug_error

# State manager
from state_manager import AgentState


MODEL = "deepseek-coder:1.3b"

# Initialize global state
state = AgentState()


def execute_tool(tool, args):

    if tool == "list_files":
        return list_files()

    elif tool == "read_file":
        return read_file(args.get("path"))

    elif tool == "write_file":
        return write_file(
            args.get("path"),
            args.get("content")
        )

    elif tool == "run_python":
        return run_python(args.get("file"))

    else:
        return "Unknown tool"


def ask_agent(prompt):

    # -----------------------------------
    # SET TASK IN STATE MANAGER
    # -----------------------------------
    state.set_task(prompt)

    # -----------------------------------
    # PROJECT ANALYZER
    # -----------------------------------
    if prompt.lower() == "analyze project":

        files = list_files()

        summary = "Project Files:\n"

        for file in files:
            summary += f"- {file}\n"

        summary += "\nFile Contents:\n"

        for file in files:
            if file.endswith(".py"):
                content = read_file(file)
                summary += f"\n--- {file} ---\n"
                summary += content[:1000]

        prompt = f"Explain this project:\n{summary}"

    # -----------------------------------
    # VECTOR MEMORY STORAGE
    # -----------------------------------
    store_memory(prompt)

    related_memory = search_memory(prompt)

    # -----------------------------------
    # CREATE PLAN (PLANNER AGENT)
    # -----------------------------------
    plan = create_plan(prompt)

    state.add_step(plan)

    # -----------------------------------
    # SYSTEM PROMPT
    # -----------------------------------
    system_prompt = f"""
You are an autonomous AI coding agent.

You have multiple capabilities:
- Planning tasks
- Writing code
- Debugging errors
- Using tools

Available tools:

1. list_files()
2. read_file(path)
3. write_file(path, content)
4. run_python(file)

If a task requires tools, respond ONLY in JSON format:

{{
"tool": "tool_name",
"args": {{}}
}}

Example:

{{
"tool": "read_file",
"args": {{"path": "main.py"}}
}}

If the task requires writing code, generate the code.

Relevant past memory:
{related_memory}

Current plan:
{plan}
"""

    # -----------------------------------
    # STORE USER MEMORY
    # -----------------------------------
    add_memory("user", prompt)

    messages = get_memory()

    messages.insert(0, {
        "role": "system",
        "content": system_prompt
    })

    # -----------------------------------
    # CALL MODEL
    # -----------------------------------
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    answer = response["message"]["content"]

    # -----------------------------------
    # TRY TOOL EXECUTION
    # -----------------------------------
    try:

        tool_data = json.loads(answer)

        tool = tool_data.get("tool")
        args = tool_data.get("args", {})

        result = execute_tool(tool, args)

        add_memory("assistant", str(result))

        state.add_history({
            "tool": tool,
            "result": result
        })

        return result

    except:
        pass

    # -----------------------------------
    # DEBUGGER AGENT
    # -----------------------------------
    if "error" in answer.lower() or "traceback" in answer.lower():

        debug_result = debug_error(answer)

        add_memory("assistant", debug_result)

        return debug_result

    # -----------------------------------
    # CODER AGENT
    # -----------------------------------
    if "write code" in prompt.lower() or "create code" in prompt.lower():

        code = generate_code(prompt)

        add_memory("assistant", code)

        return code

    # -----------------------------------
    # NORMAL RESPONSE
    # -----------------------------------
    add_memory("assistant", answer)

    state.add_history(answer)

    return answer