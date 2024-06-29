import streamlit as st
import requests
from langchain_core.messages import AIMessage, HumanMessage
import time

# app config
st.set_page_config(page_title="Streaming bot", page_icon="🤖")
st.title("Streaming bot")

def get_response(user_query, chat_history):
    # Format the chat history and user query using the provided template
    chat_history_formatted = "\n".join([f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}" for msg in chat_history])
    template = f"""
    You are a helpful assistant and your name is Ravina. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history_formatted}

    User question: {user_query}
    """

    # Prepare the payload for the request
    payload = {
        "model": "gpt-3.5-turbo",
        "version": "2024-02-01",
        "max_tokens": 500,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": template}
        ]
    }

    # Make the request to the custom endpoint
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer <OPEN_API_TOKEN.>',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        'https://<Chat_gpt_url>/openai/', 
        headers=headers, 
        json=payload
    )

    if response.status_code == 200:
        response_json = response.json()
        return response_json['response']['choices'][0]['message']['content']
    else:
        return "Error: Unable to fetch response from the server."

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a Ravina. How can I help you?"),
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
            # Placeholder for the AI response
            response_placeholder = st.empty()

            # Get the full response
            response = get_response(user_query, st.session_state.chat_history)

            # Simulate streaming by breaking down the response into chunks
            words = response.split()
            current_response = ""

            for word in words:
                current_response += word + " "
                response_placeholder.markdown(current_response)
                time.sleep(0.1)  # Adjust the speed of streaming by changing the sleep time

            # Update the chat history with the full response
            st.session_state.chat_history.append(AIMessage(content=response))
