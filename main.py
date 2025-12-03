import streamlit as st
from dashboard import show_dashboard
from fun_facts2 import show_fun_facts
from instructions import show_instructions
from compare import compare_words
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Words Across Borders",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
            
# Initialize session states that are shared across tabs
if 'search_run' not in st.session_state:
    st.session_state['search_run'] = False
if 'final_data' not in st.session_state:
    st.session_state['final_data'] = None

query_params = st.query_params
tab_from_url = query_params.get("tab", None)

# Sidebar navigation
with st.sidebar:
    default_idx = 0
    if tab_from_url == "User Manual":
        default_idx = 3
    elif tab_from_url == "Fun Facts":
        default_idx = 1
    selected_tab = option_menu(
        menu_title = "Navigation",
        options = ["Dashboard","Fun Facts","Compare Words","User Manual"],
        icons = ['file-earmark-bar-graph','bullseye','c-square','book'],
        menu_icon = 'globe-americas',
        default_index = default_idx

    )

# Route to the selected tab
if selected_tab == "Dashboard":
    show_dashboard()
elif selected_tab == "Fun Facts":
    show_fun_facts()
elif selected_tab == "User Manual":
    show_instructions()
elif selected_tab=='Compare Words':
    compare_words()