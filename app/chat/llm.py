"""
llm.py

LLM interface used by the chat system.

Responsibilities
----------------
1. Send the final prompt to Gemini.
2. Return the generated answer.

This module NEVER performs retrieval.
It ONLY communicates with the LLM.
"""

import os

from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig

from app.chat.prompts import SYSTEM_PROMPT

load_dotenv()


class ChatLLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key is None:
            raise RuntimeError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

    # ---------------------------------------------------------

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate an answer from Gemini.
        """

        response = self.client.models.generate_content(

            model=self.model,

            contents=prompt,

            config=GenerateContentConfig(

                system_instruction=SYSTEM_PROMPT,

                temperature=temperature,

            ),
        )

        if response.text is None:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()