# 🎬 AI Talking-Head Studio (D-ID)

A production-grade AI talking-head video generator powered by the D-ID API and Microsoft Azure Speech Synthesis available via both a Streamlit Web Application (Python) and a Next.js 14 Web Application (App Router, Node.js).

## 💡 Features
- **Real HTTPS Integration**: Direct integration with D-ID API (Generative AI) assuming strict polling.
- **Presenter Avatars**: Supply any direct hosted face JPEG/PNG image URL with dynamic live preview.
- **Microsoft Azure Neural Voices**: Choose from multiple natural speech voices (Jenny, Guy, Aria, etc.).
- **Live Studio Monitor**: Real-time polling with progress UI, embedded video player, and one-click MP4 download.
- **Generation History**: Display and replay past generations from your local storage.

## 🚀 Quickstart: Streamlit Web App (Python)

**1. Install Dependencies**
`pip install -r requirements.txt`

**2. Configure API Key**
Create a `.env` file in the root directory:
`D_ID_API_KEY=your_api_key_here`

**3. Run Locally**
`streamlit run app.py`
Open http://localhost:8501 in your browser.

## ☁️ Deploy to Streamlit Community Cloud (GitHub)

**1. Push to GitHub**
`git init`
`git add .`
`git commit -m "Initial commit - AI Talking-Head Studio"`
`git branch -M main`
`git remote add origin https://github.com/navneetbhatia1138-glitch/MAYBE-LAST-.git`
`git push -u origin main`

**2. Deploy on Streamlit Community Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io/) and log in.
- Click **New app** and select your GitHub repository.
- Set **Main file path** to `app.py`.
- Click **Advanced settings** -> **Secrets**, add your API key:
  `D_ID_API_KEY = "your_api_key_here"`
- Click **Deploy!**

## ⚡ Quickstart: Next.js 14 App Router (Node.js)

**1. Install Dependencies**
`npm install`

**2. Configure API Key**
Create a `.env.local` file:
`D_ID_API_KEY=your_api_key_here`

**3. Run Next.js Dev Server**
`npm run dev`
Open http://localhost:3000 in your browser.

## 🔒 Security
`D_ID_API_KEY` is strictly resolved dynamically in backend server components/route handlers. Never expose your secret key directly to client bundles.
