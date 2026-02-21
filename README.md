🐼 Your Personal AI Companion

A lightweight AI-powered web chatbot built as a personal digital companion.

Live at: https://companion-ai-1.onrender.com

✨ About

Companion-AI is a minimal AI companion designed to feel warm, personal, and interactive.

This project includes:

🌌 Animated gradient background

🧊 Glassmorphism landing card

💬 Chat interface with message animations

⌨️ Enter-to-send (desktop)

📱 Mobile responsive layout

🧠 Session-based chat memory

🔁 Auto deployment via GitHub + Render

Built as a personal gift project.

🛠 Tech Stack

Backend: Python (FastAPI)

Frontend: HTML, CSS, Vanilla JavaScript

Deployment: Render

Version Control: Git + GitHub

🚀 How to Run Locally
git clone https://github.com/NamishRajyaguru/companion_ai_1.git
cd companion_ai
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload


Then open:

http://127.0.0.1:8000

🔐 Environment Variables

Make sure to set your API key as an environment variable:

GROQ_API_KEY=your_key_here


Do NOT hardcode secrets inside the repository.

📦 Deployment

Push to GitHub

Render auto-deploys from main

Custom domain connected via DNS (CNAME + A record)

Note: Free Render instances may sleep during inactivity.

🎯 Current Features

Animated landing screen

Smooth fade transition into chat

Sliding message animations

Typing indicator

Persistent session memory (until redeploy)

Fully responsive layout

📝 Future Improvements

Persistent database storage

Smarter long-term memory

Enhanced personality tuning

Voice interaction

Custom themes

❤️ Why This Exists

Built as a meaningful digital gift.