import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from tenacity import retry, wait_exponential
from typing import List, Dict
from itertools import cycle

load_dotenv()

with open("prompt.txt") as f:
    system_prompt = f.read()

gemini_api_key_list= cycle([os.getenv("GEMINI_API_KEY1"), os.getenv("GEMINI_API_KEY2")])
gemini_api_key = next(gemini_api_key_list)
# Create the model
genai.configure(api_key=gemini_api_key)
generation_config = {
    "temperature": 0.5,
    "top_p": 0.5,
    "top_k": 40,
    "max_output_tokens": 250,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=system_prompt,
)


conversation: List[Dict[str, List[str]]] = []
total_characters: int = 0

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
async def get_ai_response(input_text: str) -> list:
    global total_characters
    global gemini_api_key

    user_input: dict = {
        "role": "user",
        "parts": [
            input_text,
        ],
    }
    conversation.append(user_input)
    total_characters = sum(len(d["parts"][0]) for d in conversation)

    while total_characters > 2000 and len(conversation) > 1:
        conversation.pop(0)

    api_speed: float = None
    chat_session = model.start_chat(history=conversation)
    try:
        start_time: float = time.time()
        response = await chat_session.send_message_async(input_text)
        api_speed = time.time() - start_time
    except Exception as e:
        check_api = next(gemini_api_key)
        if str(e) == "429 Resource has been exhausted (e.g. check quota)." and check_api is not None:
            gemini_api_key = check_api
        return False, f"There Was An Error : {e}", api_speed
    model_response: dict = {
        "role": "model",
        "parts": [
            response.text,
        ],
    }
    conversation.append(model_response)
    message: str = response.text

    return True, message, api_speed

if __name__ == "__main__":
    resp = get_ai_response("@tapu: what is the meaning of life?\n@swas: 42")
    print(resp)

    