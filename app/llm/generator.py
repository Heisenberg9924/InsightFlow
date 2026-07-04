import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiGenerator:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            if response.text is None:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text

        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}") from e