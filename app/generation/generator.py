import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  

from app.generation.prompt import build_prompt, SYSTEM_PROMPT

client = genai.Client(
    api_key = os.getenv("GENAI_API_KEY"),
)   

def generate_response(query: str, retrieved_nodes):
    prompt = build_prompt(query, retrieved_nodes)
    
    response = client.models.generate_content(
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents = prompt,
        config = {
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.2,
        },
        
    )
    
    return response.text