import streamlit as st
from engine.flows_loader import load_flows, save_flows
from pyvis.network import Network
import tempfile
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🛠 Editor de Flujos")

flows = load_flows()

# -------------------
# SELECCIÓN
# -------------------
col1, col2 = st.columns(2)

with col1:
    selected_intent = st.selectbox("Intent", list(flows.keys()))

with col2:
    selected_node = st.selectbox(
        "Nodo", list(flows[selected_intent].keys())
    )

node_data = flows[selected_intent][selected_node]

# -------------------
# TEXTO DEL NODO
# -------------------
st.subheader("📝 Texto del nodo")

text = st.text_area(
    "Contenido",
    node_data["text"],
    height=150
)

if st.button("💾 Guardar texto"):
    flows[selected_intent][selected_node]["text"] = text
    save_flows(flows)
    st.success("Texto actualizado ✔")
    st.rerun()

# -------------------
# OPCIONES
# -------------------
st.subheader("🔗 Opciones")

options = node_data.get("options", [])

# -------------------
# LISTA
# -------------------
if options:

    for opt in options:

        opt_id = opt.get("id", opt["label"])

        col1, col2, col3 = st.columns([4, 4, 1])

        new_label = col1.text_input(
            "Label",
            value=opt["label"],
            key=f"label_{opt_id}"
        )

        new_next = col2.selectbox(
            "Destino",
            options=list(flows[selected_intent].keys()),
            index=list(flows[selected_intent].keys()).index(opt["next"])
                if opt["next"] in flows[selected_intent]
                else 0,
            key=f"next_{opt_id}"
        )

        if col3.button("❌", key=f"del_{opt_id}"):
            node_data["options"] = [
                o for o in options if o.get("id") != opt_id
            ]
            save_flows(flows)
            st.rerun()

        if new_label != opt["label"] or new_next != opt["next"]:
            opt["label"] = new_label
            opt["next"] = new_next
            save_flows(flows)

else:
    st.info("Este nodo no tiene opciones aún 👀")

# -------------------
# CREAR OPCIÓN
# -------------------
st.markdown("### ➕ Crear conexión")

col1, col2 = st.columns(2)

new_label = col1.text_input("Texto botón")
new_next = col2.selectbox(
    "Nodo destino",
    list(flows[selected_intent].keys())
)

import uuid

if st.button("Agregar conexión"):
    node_data.setdefault("options", []).append({
        "id": str(uuid.uuid4()),
        "label": new_label,
        "next": new_next
    })
    save_flows(flows)
    st.success("Conexión creada 🔗")
    st.rerun()
# -------------------
# CREAR NODO
# -------------------
st.subheader("➕ Crear nodo")

new_node = st.text_input("Nombre nuevo nodo")

if st.button("Crear nodo"):
    flows[selected_intent][new_node] = {
        "text": "Nuevo nodo...",
        "options": []
    }
    save_flows(flows)
    st.success("Nodo creado 🚀")
    st.rerun()
    
# -------------------
# BORRAR NODO
# -------------------

st.subheader("🗑 Eliminar nodo")

node_to_delete = st.selectbox(
    "Selecciona nodo a eliminar",
    list(flows[selected_intent].keys()),
    key="delete_node"
)

# evitar borrar start (buena práctica)
if node_to_delete == "start":
    st.warning("No se recomienda eliminar el nodo 'start'")
else:

    # buscar referencias
    referencias = []

    for n, data in flows[selected_intent].items():
        for opt in data.get("options", []):
            if opt["next"] == node_to_delete:
                referencias.append(n)

    if referencias:
        st.error(f"⚠️ Este nodo es usado por: {referencias}")
        st.info("Debes eliminar o redirigir esas opciones primero")

    else:
        if st.button("Eliminar nodo"):
            del flows[selected_intent][node_to_delete]
            save_flows(flows)
            st.success("Nodo eliminado 💥")
            st.rerun()

# -------------------
# VISUALIZACIÓN GRAFO
# -------------------
st.markdown("## 🧭 Visualización del flujo")

def render_flow_graph(flow_data):

    net = Network(height="500px", width="100%", directed=True)

    for node_name in flow_data.keys():
        net.add_node(node_name, label=node_name)

    for node_name, node_data in flow_data.items():
        for opt in node_data.get("options", []):
            target = opt["next"]

            if target not in flow_data:
                net.add_node(target, color="red")

            net.add_edge(node_name, target, label=opt["label"])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        net.save_graph(f.name)
        return f.name

graph_file = render_flow_graph(flows[selected_intent])

with open(graph_file, "r", encoding="utf-8") as f:
    components.html(f.read(), height=550)

# -------------------
# DEBUG
# -------------------
with st.expander("🐛 Debug JSON"):
    st.json(flows)