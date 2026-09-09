import os

from dotenv import load_dotenv

load_dotenv()

from app.services.vision import client


print("Checking OpenAI configuration...")

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY is missing.")
    raise SystemExit(1)


print("OPENAI_API_KEY found.")
print("OpenAI client initialized successfully.")