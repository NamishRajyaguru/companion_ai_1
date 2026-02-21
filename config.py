import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
if not GROQ_API_KEY: 
    raise RuntimeError("GROQ_API_KEY not set")