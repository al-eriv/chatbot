import streamlit as st
from engine.chatbot_engine import detect_intent
from engine.flows_loader import load_flows, save_flows

st.title("Chatbot Instituto MVP")

# cargar flows SIEMPRE (para reflejar cambios)
flows = load_flows()

# estado inicial
if "flow" not in st.session_state:
    st.session_state.flow = None
    st.session_state.node = None
    st.session_state.last_input = None


# -------------------------
# 🛠 SIDEBAR EDITOR
# -------------------------
st.sidebar.title("🛠 Editor de Flujos")

if st.sidebar.checkbox("Modo edición"):

    edit_intent = st.sidebar.selectbox("Intent", list(flows.keys()))

    edit_node = st.sidebar.selectbox(
        "Nodo", list(flows[edit_intent].keys())
    )

    text = st.sidebar.text_area(
        "Texto del nodo",
        flows[edit_intent][edit_node]["text"]
    )

    if st.sidebar.button("Guardar cambios"):
        flows[edit_intent][edit_node]["text"] = text
        save_flows(flows)
        st.sidebar.success("Guardado ✔")
        st.rerun()  # 🔥 recarga para ver cambios


# -------------------------
# 💬 INPUT USUARIO
# -------------------------
user_input = st.text_input("Escribe tu pregunta")


# detectar intent SOLO si cambia input
if user_input and user_input != st.session_state.last_input:

    intent = detect_intent(user_input)

    if intent in flows:
        st.session_state.flow = intent
        st.session_state.node = "start"

    st.session_state.last_input = user_input


flow = st.session_state.flow
node = st.session_state.node


# -------------------------
# 🤖 CHATBOT
# -------------------------
if flow and node:

    step = flows[flow][node]

    st.write(step["text"])

    for opt in step.get("options", []):
        if st.button(opt["label"], key=f"{node}_{opt['next']}"):
            st.session_state.node = opt["next"]
            st.rerun()


# -------------------------
# DEBUG
# -------------------------
st.sidebar.json(flows)