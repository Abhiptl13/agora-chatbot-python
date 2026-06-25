from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_ai_response(prompt):

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Agora Assistant for College Lasalle. "
                        "Give short, clear, student-friendly answers. "
                        "Use bullet points when helpful. "
                        "Do not write long paragraphs. "
                        "Maximum 5 bullet points."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=180
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return "AI service is currently unavailable. Please try again later."