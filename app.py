import streamlit as st
import requests
import os
import base64
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("D_ID_API_KEY")

st.set_page_config(page_title="AI Studio", page_icon="🎬")
st.title("🎬 AI Talking-Head Studio")

uploaded_file = st.file_uploader("Upload Face Image (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Selected Avatar", width=200)

script = st.text_area("Script", "Hello! This is a test video generated from my local image upload.")

if st.button("Generate Video"):
    if not API_KEY or API_KEY == "your_actual_api_key_here":
        st.error("Please add your actual D-ID API key to the .env file first.")
        st.stop()
    if not uploaded_file:
        st.error("Please upload a JPG or PNG image first.")
        st.stop()
    if not script.strip():
        st.error("Please write a script.")
        st.stop()

    file_bytes = uploaded_file.read()
    b64_img = base64.b64encode(file_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64_img}"

    auth_header = f"Basic {API_KEY}"

    with st.spinner("Submitting image and script to D-ID..."):
        try:
            res = requests.post(
                "https://api.d-id.com/talks",
                headers={"Authorization": auth_header, "Content-Type": "application/json"},
                json={
                    "source_url": data_uri,
                    "script": {
                        "type": "text",
                        "input": script,
                        "provider": {"type": "microsoft", "voice_id": "en-US-JennyNeural"}
                    }
                }
            )
            data = res.json()
            if res.status_code != 201:
                st.error(f"D-ID API Error: {data.get('description', data)}")
                st.stop()
            talk_id = data["id"]
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
            st.stop()

    with st.spinner("Rendering video (10-20 seconds)..."):
        while True:
            poll_res = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers={"Authorization": auth_header})
            poll_data = poll_res.json()
            status = poll_data.get("status")

            if status == "done":
                st.success("Video ready!")
                st.video(poll_data.get("result_url"))
                break
            elif status in ["error", "rejected"]:
                st.error(f"Generation failed: {status}")
                break
            time.sleep(3)
