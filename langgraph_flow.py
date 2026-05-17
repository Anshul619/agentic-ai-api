"""LangGraph demo for a conditional translation workflow.

Flow:
1. Translate English input into the user-selected language.
2. If the target language is Italian, translate the result back to English.
3. Persist the Italian round-trip result to disk.
4. Otherwise, end after the first translation.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from file_store import write_translation_output
from llm_chain import make_llm
from prompts import get_translate_prompt, get_translate_to_english_prompt


class TranslationState(TypedDict, total=False):
    text: str
    language: str
    translated: str
    back_to_english: str
    output_file: str


def make_translation_graph():
    llm = make_llm()

    def translate_node(state: TranslationState) -> TranslationState:
        prompt_value = get_translate_prompt().invoke(
            {"text": state["text"], "language": state["language"]}
        )
        response = llm.invoke(prompt_value)
        return {"translated": response.content.strip()}

    def should_roundtrip(state: TranslationState) -> str:
        language = state["language"].strip().lower()
        if language == "italian":
            return "roundtrip"
        return "done"

    def translate_back_node(state: TranslationState) -> TranslationState:
        prompt_value = get_translate_to_english_prompt().invoke(
            {
                "language": state["language"],
                "translated": state["translated"],
            }
        )
        response = llm.invoke(prompt_value)
        return {"back_to_english": response.content.strip()}

    def save_node(state: TranslationState) -> TranslationState:
        saved = write_translation_output(state)
        return {"output_file": saved["output_file"]}

    graph = StateGraph(TranslationState)
    graph.add_node("translate", translate_node)
    graph.add_node("translate_back", translate_back_node)
    graph.add_node("save", save_node)

    graph.add_edge(START, "translate")
    graph.add_conditional_edges(
        "translate",
        should_roundtrip,
        {
            "roundtrip": "translate_back",
            "done": END,
        },
    )
    # graph.add_edge("translate_back", "save")
    graph.add_edge("save", END)

    return graph.compile()


def run_translation_graph(text: str, language: str) -> TranslationState:
    graph = make_translation_graph()
    return graph.invoke({"text": text, "language": language})