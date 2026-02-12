"""
LLM connector functions for GPT (OpenAI) and Gemini (Google).
"""
import json
from openai import OpenAI, APIError, RateLimitError, AuthenticationError, APIConnectionError, APIStatusError
import google.generativeai as genai
from typing import Any, Optional, Union


class LLMAPIError(Exception):
    """Raised when an LLM API call fails (rate limit, auth, server error, etc.)."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)

# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


def initialize_gpt_instance(api_key: str):
    """
    Create and return an OpenAI client instance.

    Args:
        api_key: OpenAI API key.

    Returns:
        OpenAI client instance.
    """
    return OpenAI(api_key=api_key)


def _check_gemini_response(response) -> None:
    """Raise LLMAPIError if Gemini response indicates an error (e.g. blocklist, safety)."""
    if not response.candidates:
        part = (response.prompt_feedback or getattr(response, "prompt_feedback", None))
        msg = getattr(part, "block_reason", None) or "No candidates returned"
        raise LLMAPIError(f"Gemini response error: {msg}", status_code=None)
    cand = response.candidates[0]
    if getattr(cand, "finish_reason", None) not in (None, "STOP", "MAX_TOKENS"):
        reason = getattr(cand, "finish_reason", "UNKNOWN")
        raise LLMAPIError(f"Gemini finished with reason: {reason}", status_code=None)


def _raise_gemini_api_error(e: Exception) -> None:
    """Map Gemini/Google API exceptions to LLMAPIError with status codes where possible."""
    msg = str(e)
    code = None
    if hasattr(e, "status_code"):
        code = getattr(e, "status_code", None)
    if code is None and hasattr(e, "code"):
        code = getattr(e, "code", None)
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "rate limit" in msg.lower() or "quota" in msg.lower():
        code = 429
        raise LLMAPIError(f"Gemini rate limit exceeded (429). Reduce request frequency or wait. {msg}", status_code=429) from e
    if "401" in msg or "UNAUTHENTICATED" in msg or "invalid api key" in msg.lower():
        code = 401
        raise LLMAPIError(f"Gemini authentication failed (401). Check your API key. {msg}", status_code=401) from e
    if "500" in msg or "503" in msg or "UNAVAILABLE" in msg or "INTERNAL" in msg:
        if "503" in msg:
            code = 503
        else:
            code = 500
        raise LLMAPIError(f"Gemini server error ({code}). Try again later. {msg}", status_code=code) from e
    raise LLMAPIError(f"Gemini API error: {msg}", status_code=code) from e


def initialize_gemini_instance(api_key: str):
    """
    Configure and return the Google Generative AI module (genai).
    Use the returned module to create models: genai.GenerativeModel(model_name).

    Args:
        api_key: Google AI (Gemini) API key.

    Returns:
        The configured google.generativeai module.
    """
    genai.configure(api_key=api_key)
    return genai


# ---------------------------------------------------------------------------
# Response generation
# ---------------------------------------------------------------------------


def generate_gpt_response(
    instance,
    static_query: str,
    user_query: str,
    responseClassVariable: Optional[type] = None,
    model_name: str = "gpt-4o-mini",
) -> Union[str, Any]:
    """
    Call the GPT API with a system (static) and user message.
    Optionally parse the response into a Pydantic model.

    Args:
        instance: OpenAI client from initialize_gpt_instance().
        static_query: System / static prompt (e.g. instructions).
        user_query: User message.
        responseClassVariable: Optional Pydantic model class for structured output.
        model_name: Model identifier (e.g. gpt-4o-mini, gpt-4o).

    Returns:
        If responseClassVariable is None: raw response text.
        Otherwise: parsed instance of responseClassVariable.
    """
    messages = [
        {"role": "system", "content": static_query},
        {"role": "user", "content": user_query},
    ]

    try:
        if responseClassVariable is not None:
            # Structured output: use JSON mode and parse into the given class
            response = instance.chat.completions.create(
                model=model_name,
                messages=messages,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            return responseClassVariable.model_validate(data)
        else:
            response = instance.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            return response.choices[0].message.content or ""
    except RateLimitError as e:
        status_code = getattr(e, "status_code", None) or 429
        raise LLMAPIError(
            f"GPT rate limit exceeded (429). Reduce request frequency or wait before retrying. {e!s}",
            status_code=status_code,
        ) from e
    except AuthenticationError as e:
        status_code = getattr(e, "status_code", None) or 401
        raise LLMAPIError(
            f"GPT authentication failed (401). Check your API key. {e!s}",
            status_code=status_code,
        ) from e
    except APIConnectionError as e:
        raise LLMAPIError(f"GPT connection error. {e!s}", status_code=None) from e
    except APIStatusError as e:
        code = getattr(e, "status_code", None)
        if code == 429:
            raise LLMAPIError(f"GPT rate limit exceeded (429). {e!s}", status_code=429) from e
        if code == 401:
            raise LLMAPIError(f"GPT authentication failed (401). {e!s}", status_code=401) from e
        if code in (500, 502, 503):
            raise LLMAPIError(f"GPT server error ({code}). Try again later. {e!s}", status_code=code) from e
        raise LLMAPIError(f"GPT API error: {e!s}", status_code=code) from e
    except APIError as e:
        code = getattr(e, "status_code", None)
        raise LLMAPIError(f"GPT API error: {e!s}", status_code=code) from e
    except json.JSONDecodeError as e:
        raise LLMAPIError(f"GPT returned invalid JSON for structured output: {e!s}", status_code=None) from e


def generate_gemini_response(
    instance,
    static_query: str,
    user_query: str,
    responseClassVariable: Optional[type] = None,
    model_name: str = "gemini-1.5-flash",
) -> Union[str, Any]:
    """
    Call the Gemini API with a system (static) and user prompt.
    Optionally parse the response into a Pydantic model.

    Args:
        instance: Configured genai module from initialize_gemini_instance().
        static_query: System / static prompt (e.g. instructions).
        user_query: User message.
        responseClassVariable: Optional Pydantic model class for structured output.
        model_name: Model identifier (e.g. gemini-1.5-flash, gemini-1.5-pro).

    Returns:
        If responseClassVariable is None: raw response text.
        Otherwise: parsed instance of responseClassVariable.
    """
    # Prefer system_instruction when supported (e.g. google-generativeai)
    try:
        model = instance.GenerativeModel(model_name, system_instruction=static_query)
        prompt = user_query
    except TypeError:
        model = instance.GenerativeModel(model_name)
        prompt = f"{static_query}\n\nUser: {user_query}"

    try:
        if responseClassVariable is not None:
            # Request JSON and parse into the given class
            response = model.generate_content(
                prompt,
                generation_config=instance.GenerationConfig(
                    response_mime_type="application/json",
                ),
            )
            _check_gemini_response(response)
            content = response.text
            data = json.loads(content)
            return responseClassVariable.model_validate(data)
        else:
            response = model.generate_content(prompt)
            _check_gemini_response(response)
            return response.text or ""
    except LLMAPIError:
        raise
    except json.JSONDecodeError as e:
        raise LLMAPIError(f"Gemini returned invalid JSON for structured output: {e!s}", status_code=None) from e
    except Exception as e:
        _raise_gemini_api_error(e)
