"""
exceptions.py

Custom exceptions used by the OKF Extraction Engine.
"""


class OKFExtractionError(Exception):
    """
    Base exception for all OKF extraction errors.
    """
    pass


class GeminiProviderError(OKFExtractionError):
    """
    Raised when communication with Gemini fails.
    """
    pass


class InvalidLLMResponseError(OKFExtractionError):
    """
    Raised when Gemini returns an invalid or empty response.
    """
    pass


class JSONParseError(OKFExtractionError):
    """
    Raised when the LLM response cannot be parsed as JSON.
    """
    pass


class GraphConstructionError(OKFExtractionError):
    """
    Raised when the graph cannot be constructed from the parsed response.
    """
    pass


class GraphValidationError(OKFExtractionError):
    """
    Raised when the constructed graph fails validation.
    """
    pass