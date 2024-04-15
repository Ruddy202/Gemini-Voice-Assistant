<!-- # Gemini Voice Assistant
This is a voice assistant built using Google new gemini model. 

## YouTube tutorial and preview
https://youtu.be/vfbmlRSgj9Q

<span style="color:orange">NOTE: Open AI whisper will not run on Python versions newer than 3.10. Python 3.11 and newer will not run this program.
## Authentication
Sign into your account with Bard access at https://bard.google.com/
- F12 for developer console
- Copy the values
  - Session: Go to Application → Cookies → `__Secure-1PSID` and `__Secure-1PSIDTS`. Copy the values of those.
  - Paste the values in line 10 & 11 for the token and ts_token variables inside main.py

## Installation
Clone GitHub repo.
```bash
git clone https://github.com/Ai-Austin/BardVoice
```
Change directory to bard_voice.
```bash
cd bard_voice
```
Paste your Bard Token into line 10 of the main.py file, replacing {YOUR BARD TOKEN}.
```bash
token = "{YOUR BARD TOKEN}"
```

Install Python dependencies (use pip3 if your system requires).
```bash
pip install -r requirements.txt
```
Whisper requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:
```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
## Startup Voice Assistant
```bash
python main.py
``` -->
# README: Gemini-Voice-Assistant

This repository contains code for a voice-powered AI assistant that can perform various tasks, including speech recognition, natural language generation, and more. Below, I'll provide an overview of the components and instructions for setting up and using this assistant.

Python 3.11

## Components

1. **Whisper Model (Speech Recognition)**
   - The `faster_whisper` library provides a lightweight speech recognition model.
   - It listens for a wake word (e.g., "chris") and captures audio.
   - Adjust the `whisper_size` and other parameters as needed.

2. **OpenAI API (Natural Language Generation)**
   - The `openai` library allows interaction with OpenAI's powerful language models.
   - Set your OpenAI API key in the `OPENAI_KEY` variable.

3. **Google API (Configuration)**
   - The `genai` library configures the Google API for additional functionality.
   - Replace `GOOGLE_API_KEY` with your own API key. (https://ai.google.dev/)

4. **Conversation with Gemini Model**
   - The `gemini-1.0-pro-latest` model from GenAI powers the conversation.
   - Safety settings are configured to block harmful content.
   - The model generates responses based on input.

## Usage

1. **Wake Word Detection**
   - The assistant listens for the wake word ("chris").
   - When detected, it starts capturing audio.

2. **Speech Recognition**
   - The Whisper model processes the captured audio.
   - Adjust the wake word and other parameters as needed.

3. **Natural Language Generation**
   - The OpenAI API generates responses based on user input.
   - The Gemini model provides conversational capabilities.

4. **System Messages**
   - The assistant responds to system messages (e.g., "AFFIRMATIVE").
   - Follow the instructions provided by the system.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required dependencies (Whisper, OpenAI, genai, etc.).
3. Set your API keys in the appropriate variables.
4. Run the main script to start the assistant.

## Contributions

Feel free to contribute to this project by adding new features, improving existing code, or enhancing the conversation model. Happy coding! 🚀
