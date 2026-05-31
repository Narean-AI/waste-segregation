import streamlit as st

def init_dashboard():

    if "eco_score" not in st.session_state:
        st.session_state.eco_score = 0

    if "history" not in st.session_state:
        st.session_state.history = []

def add_detection(obj):

    st.session_state.history.append(obj)

def show_dashboard():

    st.sidebar.markdown("## 🌍 Sustainability Dashboard")

    st.sidebar.metric(
        "Eco Score",
        st.session_state.eco_score
    )

    st.sidebar.metric(
        "Objects Detected",
        len(st.session_state.history)
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("### Detection History")

    for item in st.session_state.history[-5:]:
        st.sidebar.write(f"✅ {item}")