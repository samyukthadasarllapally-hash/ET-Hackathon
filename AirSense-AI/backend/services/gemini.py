import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_CONTEXT = """You are AirSense AI, an expert environmental assistant.
You help citizens and government officials understand air quality data.
Answer questions about AQI, pollution sources, health impacts, and WHO/CPCB guidelines.
Keep answers concise, accurate, and actionable."""

def ask_groq(query: str) -> str:
    if not GROQ_API_KEY:
        return (
            "Groq API key not configured. "
            "Please add GROQ_API_KEY to your .env file. "
            f"Your question was: {query}"
        )

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_CONTEXT},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
