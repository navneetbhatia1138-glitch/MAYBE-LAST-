import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("D_ID_API_KEY")
if not API_KEY and hasattr(st, "secrets") and "D_ID_API_KEY" in st.secrets:
    API_KEY = st.secrets["D_ID_API_KEY"]

st.set_page_config(page_title="AI Talking-Head Studio", page_icon="🎬", layout="centered")
st.title("🎬 AI Talking-Head Studio (D-ID)")
st.caption("Generate realistic talking-head videos with D-ID and Microsoft Azure Speech Synthesis.")

# Sidebar / Settings
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input("D-ID API Key (optional override)", value="", type="password", help="Leave blank to use environment key")
    if user_api_key:
        API_KEY = user_api_key
    
    st.markdown("---")
    voice_options = {
        "Jenny (US Female)": "en-US-JennyNeural",
        "Guy (US Male)": "en-US-GuyNeural",
        "Aria (US Female)": "en-US-AriaNeural",
        "Sonia (UK Female)": "en-GB-SoniaNeural",
        "Ryan (UK Male)": "en-GB-RyanNeural"
    }
    selected_voice_label = st.selectbox("Select Voice", list(voice_options.keys()))
    selected_voice = voice_options[selected_voice_label]

avatar_preset_list = {
    "Emma": "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.jpeg",
    "Amy": "https://create-images-results.d-id.com/DefaultPresenters/Amy_f/image.jpeg",
    "Noam": "https://create-images-results.d-id.com/DefaultPresenters/Noam_m/image.jpeg",
    "Matt": "https://create-images-results.d-id.com/DefaultPresenters/Matt_m/image.jpeg"
}

col1, col2 = st.columns([1, 2])
with col1:
    preset_choice = st.selectbox("Presenter Preset", list(avatar_preset_list.keys()))
    default_url = avatar_preset_list[preset_choice]

avatar_url = st.text_input("Avatar Image URL", default_url)
if avatar_url:
    st.image(avatar_url, caption="Presenter Preview", width=160)

script = st.text_area("Script", "Hello, welcome to the AI Talking-Head Studio powered by D-ID!", height=120)

if st.button("🚀 Generate Video", type="primary"):
    if not API_KEY:
        st.error("API Key missing! Please set D_ID_API_KEY in your .env file, Streamlit Secrets, or the sidebar.")
        st.stop()
        
    auth_header = f"Basic {API_KEY}"
    
    with st.spinner("Initiating generation with D-ID API..."):
        try:
            create_res = requests.post(
                "https://api.d-id.com/talks",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                },
                json={
                    "source_url": avatar_url,
                    "script": {
                        "type": "text",
                        "input": script,
                        "provider": {
                            "type": "microsoft",
                            "voice_id": selected_voice
                        }
                    }
                },
                timeout=30
            )
        except Exception as e:
            st.error(f"Network error initiating talk: {e}")
            st.stop()
        
        if create_res.status_code not in [200, 201]:
            st.error(f"Error ({create_res.status_code}): {create_res.text}")
            st.stop()
            
        data = create_res.json()
        talk_id = data.get("id")
        if not talk_id:
            st.error(f"Invalid response from D-ID: {data}")
            st.stop()
            
    with st.spinner("Rendering video (polling every 3 seconds)..."):
        while True:
            try:
                poll_res = requests.get(
                    f"https://api.d-id.com/talks/{talk_id}",
                    headers={"Authorization": auth_header},
                    timeout=30
                )
                poll_data = poll_res.json()
                status = poll_data.get("status")
            except Exception as e:
                st.warning(f"Polling warning: {e}. Retrying in 3 seconds...")
                time.sleep(3)
                continue
            
            if status == "done":
                result_url = poll_data.get("result_url")
                st.success("🎉 Video generation complete!")
                st.video(result_url)
                st.markdown(f"[📥 Download MP4 Video]({result_url})")
                break
            elif status in ["error", "rejected"]:
                st.error(f"Generation failed: {poll_data.get('error', 'Unknown error')}")
                break
                
            time.sleep(3)
