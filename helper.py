from waste_info import WASTE_INFO
from dashboard import add_detection

from ultralytics import YOLO
import streamlit as st
import cv2
import settings


def load_model(model_path):
    model = YOLO(model_path)
    return model


def classify_waste_type(detected_items):

    recyclable_items = set(detected_items) & set(settings.RECYCLABLE)

    non_recyclable_items = set(detected_items) & set(settings.NON_RECYCLABLE)

    hazardous_items = set(detected_items) & set(settings.HAZARDOUS)

    return (
        recyclable_items,
        non_recyclable_items,
        hazardous_items
    )


def remove_dash_from_class_name(class_name):
    return class_name.replace("_", " ")


def _display_detected_frames(model, st_frame, image):

    image = cv2.resize(image, (416, 234))

    if "last_detected" not in st.session_state:
        st.session_state["last_detected"] = set()

    if "eco_score" not in st.session_state:
        st.session_state["eco_score"] = 0

    if "history" not in st.session_state:
        st.session_state["history"] = []

    results = model.predict(
        image,
        conf=0.6,
        imgsz=416,
        verbose=False
    )

    names = model.names

    current_classes = set()

    for result in results:

        current_classes = set(
            [names[int(c)] for c in result.boxes.cls]
        )

    # Update dashboard only when detection changes
    if current_classes != st.session_state["last_detected"]:

        st.session_state["last_detected"] = current_classes

        detected_items = current_classes

        st.sidebar.markdown("# 🌍 EcoVision Dashboard")

        for item in detected_items:

            if item not in st.session_state["history"]:
                st.session_state["history"].append(item)

            add_detection(item)

            st.sidebar.success(f"📦 Detected: {item}")

            if item in WASTE_INFO:

                info = WASTE_INFO[item]

                st.sidebar.info(
                    f"""
Category: {info['category']}

Dispose: {info['dispose']}

Impact: {info['impact']}
"""
                )

                st.session_state["eco_score"] += 1

            else:

                st.sidebar.warning(
                    """
Category: 🗑 General Waste

Dispose: Municipal Waste Bin
"""
                )

        recyclable_items, non_recyclable_items, hazardous_items = (
            classify_waste_type(detected_items)
        )

        if recyclable_items:

            detected_items_str = "\n- ".join(
                remove_dash_from_class_name(item)
                for item in recyclable_items
            )

            st.sidebar.success(
                f"♻ Recyclable\n\n{detected_items_str}"
            )

        if non_recyclable_items:

            detected_items_str = "\n- ".join(
                remove_dash_from_class_name(item)
                for item in non_recyclable_items
            )

            st.sidebar.warning(
                f"🗑 Non-Recyclable\n\n{detected_items_str}"
            )

        if hazardous_items:

            detected_items_str = "\n- ".join(
                remove_dash_from_class_name(item)
                for item in hazardous_items
            )

            st.sidebar.error(
                f"☣ Hazardous\n\n{detected_items_str}"
            )

        st.sidebar.markdown("---")

        st.sidebar.metric(
            "🌱 Eco Score",
            st.session_state["eco_score"]
        )

        st.sidebar.metric(
            "📊 Objects Detected",
            len(st.session_state["history"])
        )

        st.sidebar.markdown("### 🕒 Detection History")

        for item in st.session_state["history"][-5:]:

            st.sidebar.write(f"✅ {item}")

    # Show camera frame
    plotted_frame = results[0].plot()

    st_frame.image(
        plotted_frame,
        channels="BGR"
    )


def play_webcam(model):

    source_webcam = settings.WEBCAM_PATH

    if st.button("🚀 Start Detection"):

        try:

            vid_cap = cv2.VideoCapture(source_webcam)

            st_frame = st.empty()

            while vid_cap.isOpened():

                success, image = vid_cap.read()

                if success:

                    _display_detected_frames(
                        model,
                        st_frame,
                        image
                    )

                else:

                    vid_cap.release()
                    break

        except Exception as e:

            st.sidebar.error(
                "Error loading video: " + str(e)
            )