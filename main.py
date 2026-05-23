import sys

from dotenv import load_dotenv

from langgraph_flow import run_translation_graph


class DummyFile:
    def write(self, x):
        pass

    def flush(self):
        pass


stderr_orig = sys.stderr
sys.stderr = DummyFile()


def main():
    load_dotenv()

    source_text = input("\n\n\nEnter text to translate: ")
    target_language = input("Enter target language: ")

    result = run_translation_graph(source_text, target_language)

    print("Translation:", result["translated"])
    if "back_to_english" in result:
        print("Back to English:", result["back_to_english"])
    if "output_file" in result:
        print("Saved to:", result["output_file"])


if __name__ == "__main__":
    sys.stderr = stderr_orig
    main()