import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("D_ID_API_KEY")

st.set_page_config(page_title="AI Studio", page_icon="🎬")
st.title("🎬 AI Talking-Head Studio")

avatar_url = st.text_input("Avatar Image URL", "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.jpeg")
script = st.text_area("Script", "Hello, welcome to the Streamlit D-ID Studio!")

if st.button("Generate Video"):
    if not API_KEY:
        st.error("API Key missing. Please check your .env file.")
        st.stop()
        
    auth_header = f"Basic {API_KEY}"
    
    with st.spinner("Initiating generation..."):
        create_res = requests.post(
            "https://api.d-id.com/talks",
            headers={"Authorization": auth_header, "Content-Type": "application/json"},
            json={
                "source_url": avatar_url,
                "script": {"type": "text", "input": script, "provider": {"type": "microsoft", "voice_id": "en-US-JennyNeural"}}
            }
        )
        
        if create_res.status_code != 201:
            st.error(f"Error: {create_res.json()}")
            st.stop()
            
        talk_id = create_res.json()["id"]
        
    with st.spinner("Rendering video (this takes 10-20 seconds)..."):
        while True:
            poll_res = requests.get(
                f"https://api.d-id.com/talks/{talk_id}",
                headers={"Authorization": auth_header}
            )
            status = poll_res.json().get("status")
            
            if status == "done":
                st.success("Generation Complete!")
                st.video(poll_res.json().get("result_url"))
                break
            elif status in ["error", "rejected"]:
                st.error("Generation failed.")
                break
            time.sleep(3)
