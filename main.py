import os
import json
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI
import pathlib

# 1. Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TEMP_DIR = pathlib.Path(__file__).parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# --- MEMORY STORAGE ---
HISTORY = {}

# 2. THE TEACHER BRAIN (JSON MODE)
# We force the AI to think in data structures, not just text.
SYSTEM_PROMPT = """
You are a German Language Teacher.
You must output valid JSON only. Do not speak normally.

JSON Structure:
{
  "spoken_german": "The pure German sentence for the audio. NO English. NO instructions like 'You can say'.",
  "visual_german": "The German text to show the user.",
  "english_translation": "The English translation to show in brackets."
}

Example Interaction:
User: "I am 30."
Response:
{
  "spoken_german": "Ich bin dreißig Jahre alt. Und du?",
  "visual_german": "Ich bin 30 Jahre alt. Und du?",
  "english_translation": "I am 30 years old. And you?"
}

Rules:
- Keep it simple.
- Correct mistakes gently.
- Always ask a follow-up question in German.
"""

# --- HELPERS ---
async def transcribe_voice(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = await client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

async def get_chatgpt_reply(user_id, text_input):
    if user_id not in HISTORY:
        HISTORY[user_id] = []
    
    HISTORY[user_id].append({"role": "user", "content": text_input})
    
    # Keep memory short
    if len(HISTORY[user_id]) > 10:
        HISTORY[user_id] = HISTORY[user_id][-10:]

    messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + HISTORY[user_id]
    
    # CRITICAL: We enable JSON mode here
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_payload,
        response_format={"type": "json_object"} 
    )
    
    reply_content = response.choices[0].message.content
    HISTORY[user_id].append({"role": "assistant", "content": reply_content})
    
    return json.loads(reply_content)

async def text_to_speech(text_input, file_path):
    # Speed 0.9 is clearer than 0.85
    response = await client.audio.speech.create(
        model="tts-1", 
        voice="alloy", 
        input=text_input,
        speed=0.9
    )
    response.stream_to_file(file_path)

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    HISTORY[user_id] = [] 
    await update.message.reply_text("Hallo! I am ready. Say 'I want to learn' to start.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.message.chat_id
    status_msg = None
    
    # --- PHASE 1: RECEIVE INPUT ---
    if update.message.voice:
        status_msg = await update.message.reply_text("Listening...")
        
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        user_audio_path = TEMP_DIR / f"user_{user_id}.ogg"
        await voice_file.download_to_drive(user_audio_path)
        user_text = await transcribe_voice(user_audio_path)
        
        # Get JSON Response
        ai_data = await get_chatgpt_reply(user_id, user_text)
        
        await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)

        # 1. AUDIO (Strictly the "spoken_german" part)
        bot_audio_path = TEMP_DIR / f"bot_{user_id}.mp3"
        await text_to_speech(ai_data["spoken_german"], bot_audio_path)
        await update.message.reply_voice(voice=open(bot_audio_path, 'rb'))

        # 2. TEXT (Combined Visuals)
        display_text = f"{ai_data['visual_german']} ({ai_data['english_translation']})"
        await update.message.reply_text(f"<tg-spoiler>{display_text}</tg-spoiler>", parse_mode=ParseMode.HTML)

    elif update.message.text:
        status_msg = await update.message.reply_text("Thinking...")
        user_text = update.message.text
        
        ai_data = await get_chatgpt_reply(user_id, user_text)
        
        display_text = f"{ai_data['visual_german']} ({ai_data['english_translation']})"

        await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
        await update.message.reply_text(display_text)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))
    print("JSON Bot is running...")
    app.run_polling()