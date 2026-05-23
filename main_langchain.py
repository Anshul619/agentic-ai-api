import os
import sys
from dotenv import load_dotenv
from llm_chain import make_roundtrip_runnable, translate_roundtrip

# Hide all warnings from gRPC / Abseil
class DummyFile:
    def write(self, x): pass
    def flush(self): pass

stderr_orig = sys.stderr
sys.stderr = DummyFile()  # redirect all stderr to dummy

def main():
    load_dotenv()

    runnable = make_roundtrip_runnable()

    # Take input from user
    source_text = input("\n\n\nEnter text to translate: ")
    target_language = input("Enter target language: ")

    result = translate_roundtrip(runnable, source_text, target_language)
    print("Translation:", result["translated"])
    print("Back to English:", result["back_to_english"])
    print("Saved to:", result["output_file"])

if __name__ == "__main__":
    sys.stderr = stderr_orig  # restore stderr after imports
    main()