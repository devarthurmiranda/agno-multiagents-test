from agno.agent import Agent

from config import get_model


def create_informal_agent(conversation_context: str) -> Agent:
    """Create the informal/casual specialist agent."""
    return Agent(
        name="Informal Agent",
        model=get_model(),
        add_history_to_context=True,
        additional_context=conversation_context,
        instructions="""\
You are a friendly, casual, and fun conversational assistant.

Style:
- Be warm, relaxed, and approachable.
- Use a light, conversational tone — like talking to a friend.
- Feel free to use humor when appropriate.
- Keep answers concise but engaging.
- Always respond in the same language the user is using.

You already had a brief initial conversation with the user (see context).
Continue naturally from where that conversation left off.
""",
        markdown=False,
    )
