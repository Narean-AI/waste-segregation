import streamlit as st

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="EcoVision AI",
    page_icon="♻",
    layout="wide"
)

from pathlib import Path
import helper
import settings
from dashboard import *

# Initialize dashboard
init_dashboard()

# Sidebar
st.sidebar.title("♻ EcoVision AI")

# Main Header
st.markdown("""
# ♻ EcoVision AI

### Intelligent Waste Segregation & Sustainability Assistant
""")

st.write(
    """
Detect waste objects in real-time using AI.

The system automatically:
- Detects objects
- Classifies waste type
- Suggests disposal methods
- Tracks eco score
- Shows detection history
"""
)

# Dashboard Metrics
show_dashboard()

# Custom Styling
st.markdown("""
<style>

.stRecyclable {
    background-color: rgba(233,192,78,255);
    padding: 1rem;
    border-radius: 10px;
    font-size:18px;
    margin-bottom:10px;
}

.stNonRecyclable {
    background-color: rgba(94,128,173,255);
    padding: 1rem;
    border-radius: 10px;
    font-size:18px;
    margin-bottom:10px;
}

.stHazardous {
    background-color: rgba(194,84,85,255);
    padding: 1rem;
    border-radius: 10px;
    font-size:18px;
    margin-bottom:10px;
}

</style>
""",
unsafe_allow_html=True)

# Load Model
model_path = Path(settings.DETECTION_MODEL)

try:
    model = helper.load_model(model_path)

except Exception as ex:

    st.error(
        f"Unable to load model. Check the specified path: {model_path}"
    )

    st.error(ex)

    st.stop()

# Webcam Detection
helper.play_webcam(model)

# Footer
st.sidebar.markdown("---")

st.sidebar.success(
    "🚀 AI Waste Detection Active"
)

st.sidebar.info(
    "Powered by YOLOv8"
)
