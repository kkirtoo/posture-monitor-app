# --- app.py ---
import streamlit as st
from detector import PostureDetector
from ui import show_dashboard, login

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
else:
    show_dashboard(PostureDetector())