from langchain_core.prompts import ChatPromptTemplate

def get_translate_prompt():
    system_template = "Translate the following from English into {language}"
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{text}")
        ]
    )
    return prompt_template