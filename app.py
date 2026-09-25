import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Chat Assistant")
st.caption("Codomax Internship – Module 3")

# Connect to OpenAI using a secure secret
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("OpenAI API key is not configured.")
    st.stop()

# Custom instructions
st.sidebar.header("⚙️ Custom Instructions")

system_instruction = st.sidebar.text_area(
    "How should the AI respond?",
    value="You are a helpful AI assistant. Give clear, accurate and easy-to-understand answers.",
    height=120
)

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    conversation = [
        {
            "role": "developer",
            "content": system_instruction
        }
    ]

    conversation.extend(st.session_state.messages)

    try:
        with st.chat_message("assistant"):

            response = client.responses.create(
                model="gpt-5",
                input=conversation,
                max_output_tokens=500
            )

            answer = response.output_text

            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Clear conversation
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
