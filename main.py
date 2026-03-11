from agent import ask_agent, autonomous_loop

print("Claude Agent Clone")
print("Type 'exit' to quit")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    if user_input.startswith("auto"):
        task = user_input.replace("auto ", "")
        result = autonomous_loop(task)
        print("Agent:", result)

    else:
        response = ask_agent(user_input)
        print("Agent:", response)