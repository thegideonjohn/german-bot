# 🇩🇪 German Voice & Text Tutor Bot
---

A Telegram bot powered by OpenAI that helps you practice German through natural voice conversation. Unlike standard text chatbots, this bot prioritizes listening and speaking skills.


## Features

**Voice-First Interaction:** Chat naturally. The bot listens to your voice notes and understands you perfectly.

**Native Audio Responses:** The bot replies with slow, clear German audio so you can practice listening.

**Hidden Text Translations:** Text responses are sent as "Spoilers" (blurred). You force yourself to listen first, then tap to reveal the text if you need help.

**Intelligent Correction:** The bot acts as a patient tutor, gently correcting your grammar and keeping the conversation flowing.


## How It Works

The bot uses a powerful pipeline to simulate a real human tutor:

‣ Hearing (Whisper-1): Converts your Telegram voice note into text.

‣ Thinking (GPT-4o): Analyzes your speech, checks for errors, and generates a helpful German response.

‣ Speaking (TTS-1): Converts the AI's text back into a high-quality German audio file.

‣ Delivery (Telegram): Sends the audio + a blurred text transcript back to you.


## Tech Stack

‣ Python 3.10+ installed on your machine.

‣ OpenAI API: whisper-1 (Speech to Text), gpt-4o (Logic), tts-1 (Text to Speech).

‣ A Telegram Bot Token (from @BotFather).

‣ Pydub: For audio file processing.


## Detailed Setup Instructions

### Clone the Repository

Open your terminal (Git Bash or Command Prompt)

```
git clone
```
```
git clone https://github.com/thegideonjohn/german-practice-bot.git
```
```
cd german-practice-bot
```

### Create & activate the Virtual Environment

It is best practice to use a virtual environment.

```Windows```
```
python -m venv venv
```
```
venv\Scripts\activate
```

```Mac/Linux```
```
python3 -m venv venv
```
```
source venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Create Necessary Folders
```
mkdir temp
```

### Configure API Keys

Create a new file named .env in the root folder and add your keys then save and close 

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

OPENAI_API_KEY=sk-your_openai_key_here
```

### Run the Bot

```
python main.py
```

## Usage Guide 

The bot is prompted to act as a supportive German teacher. It will not judge your mistakes but will guide you to the correct usage. It maintains context, so you can have a long, flowing conversation about your day, hobbies, or studies.

To prevent you from reading instead of listening, all text responses are hidden behind a spoiler tag.

**Step 1**: Listen to the audio response. Try to understand it.

**Step 2**: If you are stuck, tap the blurred text to reveal the written German and English translation.


## File Structure
```
.
├── main.py                # The brain of the bot (handles voice, API calls)
├── requirements.txt       # List of Python libraries needed
├── .env                   # Secrets (API Keys) - DO NOT SHARE THIS
├── .gitignore             # Tells Git what to ignore
├── README.md              # This documentation
└── temp/                  # Temporary folder for processing audio files
```


## Troubleshooting

‣ Bot stops responding? Check your terminal. 

‣ Is the script still running? Check your Internet connection.

‣ "FFmpeg not found" error? You need to install FFmpeg on your system and add it to your PATH.

‣ Windows: winget install ffmpeg then restart your terminal.

‣ OpenAI Errors? Ensure your API key has credits/billing enabled. Check the .env file to ensure there are no spaces around the = sign.


## Future Enhancements

‣  User profiles to remember your German level.

‣  Vocabulary list generation (save new words to a file).

‣  Daily conversation topic suggestions.


## License

MIT License. Viel Glück!

