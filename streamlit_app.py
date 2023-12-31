import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, BaseOutputParser
from typing import List
import os

class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text

st.title('Health and Fitness Advisor')

weight_kg = st.sidebar.text_input('Weight in kg')
height_cm = st.sidebar.text_input('Height in cm')
age = st.sidebar.text_input('Age')

def health_advisor(input_text, vector_store):
    general_model = ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0.2, model='gpt-3.5-turbo-1106')

    template = "You are an AI health and fitness advisor. You don't stop asking questions until you have all the information you need to answer with maximum accuracy based on the person's features."

    vector_store.setdefault('user_goal', []).append(f"User's weight in kg: {weight_kg}, User's height in cm: {height_cm}, User's age: {age}, User's goal: {input_text}")

    # Construct the chat prompt with vector store information
    chat_prompt = ChatPromptTemplate.from_messages([
        template,
        *vector_store.get('user_goal')
    ])

    # Invoke the model chain
    chain = chat_prompt | general_model | ParseOutput()
    response = chain.invoke(vector_store)

    st.info(response)

    # nutritional_advice_model = ChatOpenAI(openai_api_key=openai_api_key)

    # nutritional_model_template = "You are an AI nutritionist. Based on the user's goal, provide specific nutritional advice of what he should eat and what he should not eat, but no recipes. Only information about protein, vitamins, carbs, fat, etc."
    # nutri_chat_prompt = ChatPromptTemplate.from_messages([
    #     nutritional_model_template,
    #     f"{response}"
    # ])

    # nutri_chain = nutri_chat_prompt | nutritional_advice_model | ParseOutput()
    # nutri_response = nutri_chain.invoke(vector_store)

    # recipe_model = ChatOpenAI(openai_api_key=openai_api_key)

    # recipe_template = "You are an AI chef. Based on the user's goal, provide specific recipes of what he should eat and what he should not eat. You must use the nutritional advice from the previous model. You must write short and concrete list with quick foods that the user can eat to achieve his goal, nothing else. Only the list."
    # recipe_chat_prompt = ChatPromptTemplate.from_messages([
    #     recipe_template,
    #     f"Nutritional AI model response: {nutri_response}"
    # ])
    # recipe_chain = recipe_chat_prompt | recipe_model | ParseOutput()
    # recipe_response = recipe_chain.invoke(vector_store)

    # combined = response + nutri_response + recipe_response

    # conclude_model = ChatOpenAI(openai_api_key=openai_api_key)

    # conclude_template = "You are an AI health and fitness advisor. You answer with short, concrete answers, not general answers. You must take the response from the previous models and give concrete advice to the user with 2-3 sentences."

    # # Construct the chat prompt with vector store information
    # conclude_prompt = ChatPromptTemplate.from_messages([
    #     f"{conclude_template} Model response: {combined}",
    #     f"User's input: {input_text}"
    # ])


    # conclude_chain = conclude_prompt | conclude_model | ParseOutput()
    # conclude_response = conclude_chain.invoke(vector_store)


    # st.session_state.meal_vector_store = vector_store
    # st.info(conclude_response)
    # st.info(nutri_response)
    # st.info(recipe_response)

with st.form('fitness_form'):
    text = st.text_area('Enter your body goal.')
    submitted = st.form_submit_button('Submit')

    # Initialize or retrieve vector store
    vector_store = st.session_state.get('health_vector_store', {})

    if submitted and os.environ['OPENAI_API_KEY'].startswith('sk-'):
        health_advisor(text, vector_store)
        # Update the vector store for future conversations
        st.session_state.health_vector_store = vector_store