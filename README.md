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
pip install -r requirements.txt
````

## Run the script

````shell
python main.py
````

## Example Run

````
Enter text to translate: hello!
Enter target language: Italian
Translation: Ciao!
````

# Overall Flow
- Load API key and model from .env.
- Create a prompt template and a Gemini LLM instance.
- Chain them into a RunnableSequence.
- Take input from the user: source_text + target_language.
- Format the prompt with those inputs.
- Send prompt to Gemini via API.
- Receive the translation.
- Print the translation to the terminal.