from langchain_core.prompts import ChatPromptTemplate

# Placeholders {text}, {language}, {translated} must match keys on the chain dict
# (see RunnablePassthrough.assign in llm_chain.py).

def get_translate_prompt():
    system_template = "Translate the following from English into {language}"
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{text}")
        ]
    )
    return prompt_template

def get_translate_to_english_prompt():
    system_template = "Translate the following from {language} into English"
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            # {translated} comes from the first assign() step, not original {text}
            ("user", "{translated}"),
        ]
    )