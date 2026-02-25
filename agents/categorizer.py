from agno.agent import Agent
from agno.tools import Function

from config import get_model

# Mutable state used to signal routing from inside the tool call
routing_state: dict[str, str | None] = {"category": None}

VALID_CATEGORIES = ("informal", "technical")


def route_to_agent(category: str) -> str:
    """Route the conversation to a specialist agent.

    Args:
        category: Either "informal" for casual/everyday topics
                  or "technical" for programming/technical topics.
    """
    category = category.strip().lower()
    if category not in VALID_CATEGORIES:
        return (
            f"Invalid category '{category}'. "
            f"Must be one of: {', '.join(VALID_CATEGORIES)}"
        )
    routing_state["category"] = category
    return f"Routing to {category} agent."


def create_categorizer_agent() -> Agent:
    """Create the categorizer agent that talks to the user and decides routing."""
    route_function = Function.from_callable(route_to_agent)
    route_function.stop_after_tool_call = True

    return Agent(
        name="Categorizer",
        model=get_model(),
        tools=[route_function],
        add_history_to_context=True,
        instructions="""\
You are a friendly routing assistant. Your job is to figure out whether the
user needs help with something **technical** (programming, code, software,
IT, engineering, science) or something **informal** (casual chat, travel,
hobbies, daily life, general questions).

Rules:
1. Greet the user and ask how you can help.
2. If the topic is clearly technical, call route_to_agent("technical").
3. If the topic is clearly informal/casual, call route_to_agent("informal").
4. If you are NOT sure, ask a follow-up question to clarify — do NOT guess.
5. Never answer the user's actual question yourself — only categorize and route.
6. Always respond in the same language the user is using.
""",
        markdown=False,
    )
