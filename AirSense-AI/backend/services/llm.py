import os
from groq import Groq

SYSTEM_CONTEXT = """You are AirSense AI, an expert environmental assistant.
You help citizens and government officials understand air quality data.
Answer questions about AQI, pollution sources, health impacts, and WHO/CPCB guidelines.
Keep answers concise, accurate, and actionable."""

def ask_llm(query: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY not configured. Please add it to your .env file."

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_CONTEXT},
            {"role": "user",   "content": query}
        ]
    )
    return response.choices[0].message.content
