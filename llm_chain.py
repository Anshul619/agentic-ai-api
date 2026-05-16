"""LangChain LCEL translation chains.

LCEL building blocks used in this module:

  |  (pipe)
      Chains runnables left-to-right. Output of the left step is input to the right.
      Example: prompt | llm  →  dict in, AIMessage out.

  ChatPromptTemplate
      Fills {placeholders} from the input dict and returns messages for the LLM.

  StrOutputParser
      Converts the LLM AIMessage into a plain str (`.content`). Without it you get
      an object and must read `.content` yourself.

  RunnablePassthrough.assign(key=subchain)
      Keeps the incoming dict and adds one field: key = subchain.invoke(same dict).
      Step 1 input:  {"text": "...", "language": "Italian"}
      Step 1 output: {"text": "...", "language": "Italian", "translated": "Ciao!"}
      Use assign when later steps need both old and new fields.

  RunnableLambda(fn)
      Wraps a plain Python function as a Runnable so it can be piped (|) in LCEL.
      fn receives the current value (here a dict) and returns the next value.
      Used when no built-in Runnable exists (e.g. writing to LocalFileStore).
"""

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from file_store import save_translation_runnable
from prompts import get_translate_prompt, get_translate_to_english_prompt


def _make_llm():
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment or .env file")

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        google_api_key=api_key,
    )


def make_runnable():
    llm = _make_llm()
    # Single-step chain: template → Gemini → string
    return get_translate_prompt() | llm | StrOutputParser()


def make_roundtrip_runnable():
    llm = _make_llm()

    # Subchains: each is prompt | llm | StrOutputParser (dict in → str out)
    forward = get_translate_prompt() | llm | StrOutputParser()
    back = get_translate_to_english_prompt() | llm | StrOutputParser()

    return (
        # assign: run `forward`, add result as "translated"; keep text + language
        RunnablePassthrough.assign(translated=forward)
        # assign: run `back` using translated + language; add "back_to_english"
        | RunnablePassthrough.assign(back_to_english=back)
        # RunnableLambda: persist dict to disk via LocalFileStore; add "output_file"
        | save_translation_runnable()
    )


def translate(runnable, text: str, language: str) -> str:
    return runnable.invoke({"text": text, "language": language})


def translate_roundtrip(runnable, text: str, language: str) -> dict:
    out = runnable.invoke({"text": text, "language": language})
    return {
        "translated": out["translated"],
        "back_to_english": out["back_to_english"],
        "output_file": out["output_file"],
    }
