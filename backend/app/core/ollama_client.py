"""
Former Ollama client shim.

This project has migrated to Gemini. Do not call into Ollama anymore.
If any stray imports remain, switch them to:

    from app.core.gemini_client import call_gemini

Set the environment variable `GEMINI_API_KEY` before running.
"""

def call_ollama(*args, **kwargs):
    raise RuntimeError(
        "Ollama client removed. Use app.core.gemini_client.call_gemini and set GEMINI_API_KEY."
    )
