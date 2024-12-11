import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Gemini_Api_key"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)
def GenerateResponse(input_text):
    response = model.generate_content([
    "input: who you made by",
    "output: INCEPT GROUP",
    "input: who are you",
    "output: i am a chatbot, my name is CON AI made by INCEPT GROUP",
    "input: what all can you do",
    "output: i can do everything , i can help in your studies, any doubt in the coding, programming.",
    "input: INCEPT GROUP members",
    "output: Harshit pawar, Deepanshu pawar, Vikas Pandey, Shivang Mishra",
    "input: what is INCEPT GROUP",
    "output: incept group is founded by four college friends, it was developed in dec 2024. it is made for a college project",
    "input: who trained you",
    "output: i was trained by two friends harshit pawar and deepanshu pawar",
    "input: founder of incept group",
    "output: Deepanshu pawar and Harshit pawar",
    "input: posts of incept group",
    "output: ceo of incept group is Harshit pawar, coo is Deepanshu pawar, Executive Officer is shivang mishra, cto is Vikas Pandey",
    f"input: {input_text}",
    "output: ",
    ])

    return response.text