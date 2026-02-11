"""
LLM connector functions for GPT (OpenAI) and Gemini (Google).
"""

from typing import Any, Optional, Union

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
    from openai import OpenAI
    return OpenAI(api_key=api_key)


def initialize_gemini_instance(api_key: str):
    """
    Configure and return the Google Generative AI module (genai).
    Use the returned module to create models: genai.GenerativeModel(model_name).

    Args:
        api_key: Google AI (Gemini) API key.

    Returns:
        The configured google.generativeai module.
    """
    import google.generativeai as genai
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

    if responseClassVariable is not None:
        # Structured output: use JSON mode and parse into the given class
        response = instance.chat.completions.create(
            model=model_name,
            messages=messages,
            response_format={"type": "json_object"},
        )
        import json
        content = response.choices[0].message.content
        data = json.loads(content)
        return responseClassVariable.model_validate(data)
    else:
        response = instance.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        return response.choices[0].message.content or ""


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

    if responseClassVariable is not None:
        # Request JSON and parse into the given class
        response = model.generate_content(
            prompt,
            generation_config=instance.GenerationConfig(
                response_mime_type="application/json",
            ),
        )
        import json
        content = response.text
        data = json.loads(content)
        return responseClassVariable.model_validate(data)
    else:
        response = model.generate_content(prompt)
        return response.text or ""
