import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
import requests
import os
from datetime import datetime
import random
import logging
from stt import STT
from random import sample
import asyncio
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
import g4f
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram import F
from aiogram import types
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from pathlib import Path
from aiogram.types.input_file import InputFile
stt = STT()



model = Model(r'vosk/ru')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()



def recognize_speak():
    while True:
        data = stream.read(120000)
        rec.AcceptWaveform(data)
        x=json.loads(rec.Result())
        if x["text"] == "":
            continue
        else:
            return x["text"]


HELP_STR = '''/start - Начало работы
/help - Помощь
'''



bot = Bot(token="YOUR_TOKEN")
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Диспетчер
dp = Dispatcher()





###### ADMINS ##############



######### ADDITIONAL #######################
@dp.message(Command("start"))
async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, (f"👋 Привет {msg.from_user.full_name}! Ты можешь мне задать свой вопрос\nМои команды ты можешь узнать в /help\n\n 😤 А если возникнут трудности, то всегда пожалуйста к t.me/papyas_07"))

@dp.message(Command("id"))
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, '🪪 Ваш ID: '+str(msg.from_user.id))

@dp.message(Command("help"))
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, HELP_STR)

@dp.message(Command("ping"))
async def pong(msg: types.Message):
    await bot.send_message(msg.from_user.id, "⚪ pong")

@dp.message(Command("whoiam"))
async def whoiam(msg: types.Message):
    text = f"👀 Твое имя: {msg.from_user.full_name}, твой ник: {msg.from_user.username}"
    await bot.send_message(msg.from_user.id, text)

@dp.message()
async def echo(msg: types.Message):
    if msg.content_type == types.ContentType.VOICE or msg.content_type == types.ContentType.AUDIO or msg.content_type == types.ContentType.DOCUMENT:
        if msg.content_type == types.ContentType.VOICE:
            file_id = msg.voice.file_id
        elif msg.content_type == types.ContentType.AUDIO:
            file_id = msg.audio.file_id
        elif msg.content_type == types.ContentType.DOCUMENT:
            file_id = msg.document.file_id
        else:
            await msg.reply("Формат документа не поддерживается")
            return
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_on_disk = Path("", f"{file_id}.tmp")
        await bot.download_file(file_path, destination=file_on_disk)

        text = stt.audio_to_text(file_on_disk)
        if not text:
            text = "😢 Формат документа не поддерживается"
            return
        os.remove(file_on_disk)  # Удаление временного файла
    else: text=''
    if text: uni_text=text
    else: uni_text=msg.text
    temp = await msg.reply( f"⏰ Сейчас подумаю!")
    response = await g4f.ChatCompletion.create_async(model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": uni_text}], tempetarure=0.7)
    await temp.delete()
    await msg.reply(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())