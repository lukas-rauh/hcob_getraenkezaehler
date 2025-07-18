import streamlit as st
import json
import os
from PIL import Image

DATA_FILE = "data.json"
EURO_PRO_EINHEIT = 2

# ----------- Datei initialisieren und laden -----------

def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------- Initialisieren -----------

init_data()
data = load_data()

# ----------- Custom Styling -----------

st.set_page_config(page_title="Gruppenzähler", layout="wide")

st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #45a049;
    }

    h1, h2, h3 {
        color: #2e7d32;
    }

    div[data-testid="stExpander"] div[role="button"] {
        background-color: #e8f5e9;
    }

    </style>
""", unsafe_allow_html=True)

# ----------- Kopfzeile mit Logo -----------

col1, col2 = st.columns([1, 5])
with col1:
    logo = Image.open("logo.png")
    st.image(logo, use_container_width=200)
with col2:
    st.markdown("## 🍻 Gruppenzähler für die Bierliste")
    st.markdown("Zähle, wer was trinkt – und behalte den Überblick über die Kosten.")

st.divider()

# ----------- Gruppenwahl & neue Gruppe -----------

group_names = list(data.keys())
selected_group = st.selectbox("📂 Wähle eine Gruppe", group_names)

with st.expander("➕ Neue Gruppe erstellen"):
    new_group = st.text_input("Name der neuen Gruppe")
    if st.button("Gruppe hinzufügen") and new_group:
        if new_group not in data:
            data[new_group] = {}
            save_data(data)
            st.success(f"Gruppe '{new_group}' wurde erstellt!")
            st.rerun()
        else:
            st.warning("Diese Gruppe existiert bereits.")

# ----------- Gruppenansicht -----------

if selected_group:
    st.header(f"👥 Gruppe: {selected_group}")
    group_data = data[selected_group]

    total = 0

    for name in group_data:
        cols = st.columns([4, 1, 2])
        with cols[0]:
            st.write(f"**{name}**")
        with cols[1]:
            if st.button(f"➕ {group_data[name]}", key=f"{name}_{selected_group}"):
                group_data[name] += 1
                data[selected_group] = group_data
                save_data(data)
                st.rerun()
        with cols[2]:
            betrag = group_data[name] * EURO_PRO_EINHEIT
            st.write(f"{betrag} €")
            total += betrag

    st.markdown("---")
    st.markdown(f"### 💶 Gesamtsumme: **{total} €**")

    # ----------- Namen hinzufügen -----------

    with st.expander("➕ Neuen Namen zur Gruppe hinzufügen"):
        new_name = st.text_input("Neuer Name", key="name_input")
        if st.button("Name speichern"):
            if new_name and new_name not in group_data:
                group_data[new_name] = 0
                data[selected_group] = group_data
                save_data(data)
                st.success(f"'{new_name}' wurde hinzugefügt.")
                st.rerun()
            elif new_name in group_data:
                st.warning("Dieser Name existiert bereits in der Gruppe.")
