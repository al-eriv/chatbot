import streamlit as st
from engine.chatbot_engine import detect_intent
from engine.flows import FLOWS

st.title("Chatbot Instituto MVP")

if "flow" not in st.session_state:
    st.session_state.flow = None
    st.session_state.node = None


user_input = st.text_input("Escribe tu pregunta")


if user_input:

    intent = detect_intent(user_input)

    if intent in FLOWS:
        st.session_state.flow = intent
        st.session_state.node = "start"

node = st.session_state.node
flow = st.session_state.flow


if flow and node:

    step = FLOWS[flow][node]

    st.write(step["text"])

    for option, next_node in step["options"].items():

        if st.button(option):

            st.session_state.node = next_node
            st.rerun()