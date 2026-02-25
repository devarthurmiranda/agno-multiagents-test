from agno.models.google import Gemini


def get_model() -> Gemini:
    """Return a shared Gemini model instance.

    GOOGLE_API_KEY is read from the environment automatically.
    """
    return Gemini(id="gemini-2.0-flash")
