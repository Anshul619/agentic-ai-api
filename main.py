import os
import sys
from dotenv import load_dotenv
from llm_chain import make_runnable, translate

# Hide all warnings from gRPC / Abseil
class DummyFile:
    def write(self, x): pass
    def flush(self): pass

stderr_orig = sys.stderr
sys.stderr = DummyFile()  # redirect all stderr to dummy

def main():
    load_dotenv()

    runnable = make_runnable()

    # Take input from user
    source_text = input("\n\n\nEnter text to translate: ")
    target_language = input("Enter target language: ")

    output = translate(runnable, source_text, target_language)
    print("Translation:", output)

if __name__ == "__main__":
    sys.stderr = stderr_orig  # restore stderr after imports
    main()