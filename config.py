from agno.db.in_memory.in_memory_db import InMemoryDb
from agno.models.google import Gemini

# Shared in-memory database — persists for the lifetime of the process.
# All agents share this instance so sessions/history stay in RAM.
memory_db = InMemoryDb()


def get_model() -> Gemini:
    """Return a shared Gemini model instance.

    GOOGLE_API_KEY is read from the environment automatically.
    """
    return Gemini(id="gemini-2.0-flash")
