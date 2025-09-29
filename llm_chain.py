import os
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import get_translate_prompt

def make_runnable():
    prompt = get_translate_prompt()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment or .env file")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        google_api_key=api_key
    )

    # Runnable pipeline: prompt → model
    runnable = prompt | llm
    return runnable

def translate(runnable, text: str, language: str) -> str:
    result = runnable.invoke({"text": text, "language": language})
    return result.content