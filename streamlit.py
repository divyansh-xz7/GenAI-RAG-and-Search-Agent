from langchain_community.callbacks.streamlit import ( StreamlitCallbackHandler)
import streamlit as st
from LLM.agent import agent_executor
from utils.chat_summarizer import summarize
from utils.streamlist_chat_history import chat_history

prompt =''


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        print(chat_history)
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke({'input':prompt, 'chat_history':chat_history}, {'callbacks':[st_callback]})
        chat_history += response['input'] + response['output']
        print(chat_history) 
        st.write(response['output'])