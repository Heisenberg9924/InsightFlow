"""
llm.py

Gemini provider for Open Knowledge Format (OKF) extraction.

Responsibilities
----------------
1. Build the extraction prompt.
2. Send it to Gemini.
3. Return the raw JSON response.

This module DOES NOT:

- Parse JSON
- Validate responses
- Build graphs
- Store data
"""

import os

from dotenv import load_dotenv

load_dotenv()

from app.okf.extractor.exceptions import (
    GeminiProviderError,
    InvalidLLMResponseError,
)

from google import genai
from google.genai.types import GenerateContentConfig

from app.okf.prompts import (
    SYSTEM_PROMPT,
    build_extraction_prompt,
)


class GeminiProvider:
    """
    Handles communication with Gemini for OKF extraction.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise GeminiProviderError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

    def generate(
        self,
        text: str,
        temperature: float = 0.0,
    ) -> str:
        """
        Generate raw OKF JSON from a document chunk.

        Parameters
        ----------
        text : str
            Document chunk.

        temperature : float
            Sampling temperature.

        Returns
        -------
        str
            Raw JSON string returned by Gemini.
        """

        prompt = build_extraction_prompt(text)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=temperature,
            ),
        )

        if not response or not response.text:
            raise InvalidLLMResponseError(
                "Gemini returned an empty response."
            )

        return response.text.strip()