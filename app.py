import openai
import os 
from streamlit_chat import message
import streamlit as st

openai.api_key = os.getenv("HF_API_KEY")
openai.api_base = "https://limcheekin-mistral-7b-instruct-v0-1-gguf.hf.space/v1"

def get_prompt(
        system_prompt: str, 
        instruction: str):
    prompt = f"<s>[INST]System: {system_prompt}[/INST]</s> [INST]User: {instruction}[/INST]"
    return prompt

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant, you will complete the task by follow the instructions given."

def get_completion(
        prompt, 
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        temperature=0.0, 
        max_tokens=800):
    messages = [{"role": "user", "content": get_prompt(
        system_prompt=system_prompt, 
        instruction=prompt)}]
    response = openai.ChatCompletion.create(
        model="",
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
        request_timeout=600,
    )
    assistant_content = response['choices'][0]['message']['content']
    
    return assistant_content

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Mistral 7B Chatbot")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
user_input = st.chat_input("What would you like to know?")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get bot response (Assuming your get_completion function returns the response text)
    bot_response = get_completion(user_input)
    
    # Display bot response in chat message container
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
