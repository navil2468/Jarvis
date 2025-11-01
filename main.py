from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from RealtimeSTT import AudioToTextRecorder
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

MAX_OUTPUT_TOKENS = 50

def main():
    load_dotenv()

    #Loading GeminiAPIKey
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    if not gemini_api_key:
        raise ValueError("api_key environmental var not properly established!")
    if not elevenlabs_api_key:
        raise ValueError("api_key environmental var not properly established!")

    print("API Key is working ")
    
    client = genai.Client(api_key=gemini_api_key)
    elevenlabs = ElevenLabs(
        api_key=elevenlabs_api_key,
    )

    #Create Chat with Jarvis
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            system_instruction="My name is Navil",
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            ),
            max_output_tokens=MAX_OUTPUT_TOKENS
        )
    )
    
    # Audio to Text
    recorder = AudioToTextRecorder(model='tiny.en', language='en', spinner='False')


    # Run whatever is said to Jarvis
    while True:
        #txt = input("You: ")
        print("You: ", end="")
        txt = recorder.text()
        print(txt)
        if txt.lower() in ["go to sleep.", "shut down.", "exit."]:
            break
        response = chat.send_message_stream(txt)
        full_response = []

        print("Jarvis: ", end="")
        for wrd in response:
            print(wrd.text, end="")
            full_response.append(wrd.text)
        
        full_response_text = ''.join(full_response).strip()
        print()
        if full_response_text:
            audio = elevenlabs.text_to_speech.convert(
                text=full_response_text,
                voice_id="FoKAplwbWpBarMO157Q7",
                model_id="eleven_flash_v2_5",
                output_format="mp3_44100_128"
            )
            play(audio)

    recorder.shutdown()

if __name__ == "__main__":
    main()