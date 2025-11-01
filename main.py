from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("api_key environmental var not properly established!")

client = genai.Client(api_key=api_key)
print("API Key is working ")

chat = client.chats.create(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        system_instruction="My name is Navil",
        thinking_config=types.ThinkingConfig(
            thinking_budget=0
        )
    )
)

while True:
    txt = input("You: ")
    if txt.lower() in ["exit", "done", "quit"]:
        break
    response = chat.send_message_stream(txt)
    print("Jarvis: ", end="")
    for wrd in response:
        print(wrd.text, end="")
    print()

