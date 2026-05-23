"""Persist translation results with LangChain LocalFileStore.

  LocalFileStore (langchain_classic.storage)
      Key-value store backed by files on disk. mset([(key, bytes)]) writes one file
      per key under OUTPUT_DIR. Keys must match [a-zA-Z0-9_.-/]+.

  RunnableLambda(fn)
      Turns write_translation_output into a Runnable so it can be the last step in
      the LCEL pipe (|). fn gets the full state dict and must return a dict (we add
      output_file while keeping translated, back_to_english, etc.).
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from langchain_classic.storage import LocalFileStore
from langchain_core.runnables import RunnableLambda

DEFAULT_OUTPUT_DIR = "data"
OUTPUT_KEY = "latest_translation.json"


def get_output_dir() -> Path:
    return Path(os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR))


def get_output_path() -> Path:
    return get_output_dir() / OUTPUT_KEY


def get_file_store(root_path: Path | None = None) -> LocalFileStore:
    path = root_path or get_output_dir()
    path.mkdir(parents=True, exist_ok=True)
    return LocalFileStore(path)


def _serialize_roundtrip(state: dict) -> bytes:
    payload = {
        "source_text": state["text"],
        "target_language": state["language"],
        "translated": state["translated"],
        "back_to_english": state["back_to_english"],
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def write_translation_output(state: dict) -> dict:
    """Called by RunnableLambda: write JSON bytes to disk, return state + path."""
    store = get_file_store()
    store.mset([(OUTPUT_KEY, _serialize_roundtrip(state))])
    return {**state, "output_file": str(get_output_path().resolve())}


def save_translation_runnable() -> RunnableLambda:
    # Wraps write_translation_output so llm_chain can pipe: ... | save_translation_runnable()
    return RunnableLambda(write_translation_output)
