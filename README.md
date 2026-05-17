# LangChain

[LangChain](https://python.langchain.com/docs/tutorials/llm_chain/) is a framework to chain together prompts, models, and logic. It provides:
- Prompt templates → cleanly define input structure
- Chains / Runnables → connect prompts to LLMs
- Input/output management → automatically handle variables
- Async, caching, logging, etc. → optional advanced features

In this project, LangChain is the glue between user input and Gemini API calls.

Without LangChain, we have to manually:
- Format the prompt string with your variables.
- Make an HTTP request to the Gemini API.
- Extract the generated text from the JSON response.

LangChain automates all of that.

# Quick start

## Git Clone

````shell
git clone langchain_gemini_llmchain
cd langchain_gemini_llmchain
````

## Setup environment variables
- Copy the example environment file and update it as needed
- Add **GEMINI_API_KEY** if you want generative answers

````shell
cp .env.example .env
````

## Create and activate virtual environment

````shell
python3 -m venv .venv
source .venv/bin/activate
````

## Install dependencies

````shell
pip3 install -r requirements.txt
````

## Run the script

````shell
python3 main.py
````

## Run the LangGraph demo

````shell
python3 main_langgraph.py
````

## Example Run

````
Enter text to translate: hello!
Enter target language: Italian
Translation: Ciao!
Back to English: Hello!
Saved to: /path/to/data/latest_translation.json
````

# Overall Flow
- Load API key and model from .env.
- Create forward and reverse prompt templates and a shared Gemini LLM instance.
- Chain them into a round-trip RunnableSequence with `RunnablePassthrough.assign`.
- Take input from the user: source_text + target_language.
- Forward step: format the prompt (English → target language) and send to Gemini.
- Assign the translation to `translated`.
- Back step: format the reverse prompt (target language → English) and send to Gemini.
- Assign the result to `back_to_english`.
- Print both the forward translation and the English round-trip to the terminal.
- Persist results with LangChain `LocalFileStore` (`data/latest_translation.json` by default; override with `OUTPUT_DIR`).

# LangGraph Demo Flow
- Build a `StateGraph` with explicit workflow nodes instead of an LCEL runnable chain.
- `translate` node: translate English input into the requested language.
- Conditional branch: if the target language is Italian, continue to a round-trip path.
- `translate_back` node: translate the Italian output back into English.
- `save` node: persist the Italian round-trip result to `data/latest_translation.json`.
- For any non-Italian language, the graph ends after the first translation.