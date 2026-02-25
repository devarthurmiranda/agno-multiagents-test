"""Multi-Agent Routing System using Agno + Gemini."""

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from agents import (
    create_categorizer_agent,
    create_informal_agent,
    create_technical_agent,
    routing_state,
)

load_dotenv()

console = Console()
EXIT_COMMANDS = {"exit", "quit", "bye"}


def build_conversation_summary(history: list[dict]) -> str:
    """Build a text summary of the categorization conversation."""
    lines: list[str] = []
    for msg in history:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if content:
            lines.append(f"{role}: {content}")
    return "\n".join(lines)


def print_assistant(name: str, text: str) -> None:
    console.print(f" [bold cyan]{name}:[/bold cyan] {text}")


def run() -> None:
    console.print(
        Panel(
            Text("Multi-Agent Routing System", justify="center", style="bold magenta"),
            subtitle="Agno + Gemini",
        )
    )

    # --- Phase 1: Categorization ---
    categorizer = create_categorizer_agent()
    conversation_history: list[dict] = []

    console.print("\n[dim]Type 'exit', 'quit', or 'bye' to leave.[/dim]\n")

    while routing_state["category"] is None:
        user_input = Prompt.ask(" [bold green]You[/bold green]")
        if user_input.strip().lower() in EXIT_COMMANDS:
            console.print("\n[bold]Bye! :wave:[/bold]")
            return

        conversation_history.append({"role": "user", "content": user_input})

        response = categorizer.run(user_input)
        assistant_text = response.content

        # If the model routed, there may still be a textual reply before the tool call
        if assistant_text:
            conversation_history.append(
                {"role": "assistant", "content": assistant_text}
            )
            print_assistant("Categorizer", assistant_text)

        # Check if routing happened
        if routing_state["category"] is not None:
            break

    category = routing_state["category"]
    console.print(
        f"\n[bold yellow]>>> Routed to"
        f" {'Technical' if category == 'technical' else 'Informal'}"
        f" Agent <<<[/bold yellow]\n"
    )

    # --- Transition: build context for the specialist ---
    context_summary = build_conversation_summary(conversation_history)

    if category == "technical":
        specialist = create_technical_agent(context_summary)
        agent_label = "Technical Agent"
    else:
        specialist = create_informal_agent(context_summary)
        agent_label = "Informal Agent"

    # --- Phase 2: Specialist conversation ---
    while True:
        user_input = Prompt.ask(" [bold green]You[/bold green]")
        if user_input.strip().lower() in EXIT_COMMANDS:
            console.print("\n[bold]Bye! :wave:[/bold]")
            return

        response = specialist.run(user_input)
        if response.content:
            print_assistant(agent_label, response.content)


if __name__ == "__main__":
    run()
