from agent import ask_agent
from rich import print

print("\n[bold cyan]Claude Agent Clone[/bold cyan]")
print("[yellow]Type 'exit' to quit[/yellow]\n")

while True:

    user_input = input("[bold green]You:[/bold green] ")

    if user_input.lower() == "exit":
        break

    response = ask_agent(user_input)

    print("\n[bold blue]AI:[/bold blue]", response)