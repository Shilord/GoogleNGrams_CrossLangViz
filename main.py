import streamlit as st
from dashboard import show_dashboard
from fun_facts import show_fun_facts
from instructions import show_instructions

st.set_page_config(
    page_title="Linguistic Trends Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session states that are shared across tabs
if 'search_run' not in st.session_state:
    st.session_state['search_run'] = False
if 'final_data' not in st.session_state:
    st.session_state['final_data'] = None

# Sidebar navigation
with st.sidebar:
    st.title("🌍 Navigation")
    selected_tab = st.radio(
        "Select a page:",
        ["📊 Dashboard", "🎯 Fun Facts", "📖 Instructions"],
        label_visibility="collapsed"
    )

# Route to the selected tab
if selected_tab == "📊 Dashboard":
    show_dashboard()
elif selected_tab == "🎯 Fun Facts":
    show_fun_facts()
elif selected_tab == "📖 Instructions":
    show_instructions()