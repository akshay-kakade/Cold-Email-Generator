# chain.py
import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_email(job_description: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Set it in Streamlit Secrets.")

    # Replace with your own LLM API request
    response = requests.post(
        "https://api.groq.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": "You are an expert cold email writer."},
                {"role": "user", "content": f"Write a cold email for this job:\n{job_description}"}
            ],
            "temperature": 0.7
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Groq API Error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
