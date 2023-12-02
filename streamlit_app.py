import streamlit as st
from langchain.llms import OpenAI, GPT3, DialoGPT
from langchain.chat_models import ChatOpenAI

from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate






st.title('Task Planner')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
joke_type = st.sidebar.text_input('Joke Type')

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    chat_model = ChatOpenAI()
    joke_prompt = f"Generate a {joke_type.lower()} joke: {input_text}"
    joke_response = llm(joke_prompt)

    messages = [HumanMessage(content=text)]
    respomse = chat_model.invoke(messages)

    st.info(respomse)




with st.form('my_form'):
    text = st.text_area('Enter keywords or topics for your joke.')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)