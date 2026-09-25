import streamlit as st
from google import genai

st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖")

st.title("🤖 AI Chat Assistant")
st.caption("Codomax Internship – Module 3")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.sidebar.header("⚙️ Custom Instructions")

instruction = st.sidebar.text_area(
    "How should the AI respond?",
    "You are a helpful AI assistant. Give clear and easy-to-understand answers."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages
    )

    prompt = f"""
{instruction}

Conversation:
{history}

Respond to the latest user message.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        answer = response.text

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        st.error(f"Error: {e}")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
