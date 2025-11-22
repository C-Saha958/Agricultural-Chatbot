# 🌾 AgriBot: Multilingual Crop Assistant (FastAPI + Groq)

AgriBot is a high-performance, voice-enabled conversational AI assistant designed to provide real-time, expert advice on agriculture, crops, diseases, and farming techniques. It leverages the speed of Groq's inference engine and supports multilingual communication to maximize accessibility for a diverse user base.

##  Key Features

* **Multilingual Support:** Supports conversation in **English, Hindi, Hinglish (Hindi + English mix), and Bengali**. The LLM automatically detects the user's language and responds accordingly.
* **Voice Input (STT):** Allows users to speak their queries using the microphone, which is transcribed into text using localized Speech-to-Text (STT) services (`hi-IN` optimized).
* **Low-Latency AI:** Built on the Groq inference engine for near-instantaneous, high-speed responses.
* **Domain Expertise:** Specialized in accurate crop disease diagnosis, fertilizer advice, and actionable farming recommendations (providing both organic and chemical remedies).
* **Modular Architecture:** Separates the frontend, API, and core services for robust scaling and maintenance.

##  Architecture Overview

The AgriBot system is structured into three main components:

1.  **Client Layer (Gradio):** Provides the interactive web interface, handles user chat state, and captures microphone audio.
2.  **API Layer (FastAPI):** Acts as a high-performance HTTP router and orchestrator, handling requests for chat and speech-to-text.
3.  **Service Layer (Python Modules):** Contains the core logic, including communication with the Groq LLM (using the `llama-3.3-70b-versatile` model) and local audio processing.



##  How It Works: Data Flow

The application handles two main types of user input, both routed through the FastAPI backend to ensure resilience and separation of concerns.

### 1. Voice Input Flow (STT)

This process converts spoken audio into the text that appears in the input box.

1.  **Gradio Captures:** User records audio via the microphone component in `gradio_app.py`.
2.  **Frontend Prepares:** `gradio_app.py` reads the audio file and encodes it into a Base64 string.
3.  **API Call:** The frontend sends the Base64 audio to the **`/api/v1/speech-to-text`** FastAPI endpoint (`routes_voice.py`).
4.  **Backend Transcribes:** The endpoint decodes the Base64 back to raw audio bytes and sends them to the `voice_service.py` which uses the Google STT engine (optimized for `hi-IN`).
5.  **Result Displayed:** The resulting transcribed text is returned and automatically fills the Gradio text input box.

### 2. Text Chat Flow (LLM Generation)

This process executes after the user submits text (either typed or transcribed).

1.  **Gradio Submits:** The user submits the text, triggering the `chat_function` in `gradio_app.py`.
2.  **History Management:** The `chat_function` appends the new message and trims the conversation history (keeping the last 10 turns) using the `gr.State` component.
3.  **API Call:** The frontend sends the trimmed **history** array to the **`/api/v1/chat`** FastAPI endpoint (`routes_chat.py`).
4.  **LLM Context:** The endpoint calls `groq_service.py`, which constructs the final prompt by prepending the **AgriBot System Prompt** and including the conversation history for context.
5.  **Groq Inference:** The `groq_service.py` securely calls the Groq API with the full message context, using the high-speed `llama-3.3-70b-versatile` model.
6.  **Response Displayed:** The generated text reply is returned and appended to the Gradio chatbot UI.



##  Setup and Installation

### Prerequisites

1.  **Python 3.8+**
2.  **Groq API Key:** Required for LLM inference.

### 1. Clone the Repository

Navigate to the directory where you want to place the project and clone it:


git clone <YOUR_REPO_URL>
cd <YOUR_REPO_NAME>/backend/
2. Set Up Environment
We strongly recommend using a virtual environment.



# Create a virtual environment
python -m venv venv 

# Activate the virtual environment
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\activate   # Windows
3. Install Dependencies
Install all required Python packages:



pip install fastapi uvicorn requests gradio python-multipart gtts speechrecognition
4. Configure API Key (Security)
To keep your Groq API Key secure, create a file named .env in the backend/ directory (the same location as this README.md) and add your key:

# .env (DO NOT COMMIT THIS FILE TO GITHUB)
GROQ_API_KEY="paste_your_key_here"
## Running the Application
The application requires two separate processes to run simultaneously: the FastAPI Backend and the Gradio Frontend.

Step 1: Start the Backend API
This process exposes the /api/v1/chat and /api/v1/speech-to-text endpoints.



uvicorn app.main:app --reload --port 8000
The backend will now be running at http://127.0.0.1:8000.

Step 2: Start the Gradio Frontend
In a new terminal window (with the virtual environment active and still in the backend/ directory), start the frontend:



python gradio_app.py
The application will launch in your browser, typically at http://127.0.0.1:7860 (or a similar address).

# Security Note on API Keys
The .gitignore file is configured to exclude the .env file from version control. NEVER remove .env from the .gitignore list or commit files containing sensitive keys. This is critical for maintaining the security of your GROQ_API_KEY.

##  Future Enhancements
The project is planned for further expansion with the following features:

Image Recognition for Disease Detection: Integrate a computer vision model to analyze images of diseased crops uploaded by users, providing visual and diagnosis confirmation.

Real-time Weather-Based Suggestion: Utilize external weather APIs to provide context-aware suggestions, such as adjusting planting/irrigation schedules based on local climate data.
