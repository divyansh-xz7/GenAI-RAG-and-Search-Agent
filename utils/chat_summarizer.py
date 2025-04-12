from LLM.llm import GROQ_LLM


def summarize(conv):
    prompt = f"You are an expert human-ai chat summarizer. \nYou will be given an json like string which contains three parts 'input' is the user query, 'output' is the AI response, and 'chat_history' which is summary of past chats which may or may not be empty. \nNow generate a new consice and crisp summary containing all necessary information/details/keywords to retain the context of conversation. \nOutput Format : new summary in plain text\n\n\nConversation : {conv}"

    new_summary = GROQ_LLM.predict(prompt)
    print(new_summary)
    return new_summary
