memory = []

def add_memory(role, content):
    memory.append({
        "role": role,
        "content": content
    })

def get_memory():
    return memory