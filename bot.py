import datetime
import requests
import wikipedia

from config import tg_bot_token, open_weather_token

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType, Message

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

# Команды 
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello fucking world!")

@dp.message_handler(commands=["who_is_god"])
async def start_command(message: types.Message):
    await message.reply("Ильхам")


@dp.message_handler(commands=["github"])
async def start_command(message: types.Message):
    await message.reply("https://github.com/titanilham/bot-weather-telegram")
    
@dp.message_handler(commands=["GitHub"])
async def start_command(message: types.Message):
    await message.reply("https://github.com/titanilham/bot-weather-telegram")

@dp.message_handler(commands=["your_maker"])
async def start_command(message: types.Message):
    await message.reply("Мой создатель Мухаметгалеев Ильхам \U0001F970")


@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply("""Напиши название города или же вопрос после моего имени.
                        
Список комманд:
/start
/help
/info
/GitHub
/your_maker
/who_is_god
                        """)

@dp.message_handler(commands=["info"])
async def start_command(message: types.Message):
    await message.reply("Я AexissBot")


# Приветствие 
@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    await bot.send_message(message.chat.id, f"Приветствую вас, юный кодер, напишите о себе, {new_member.mention}")


# Обработка сообщений
@dp.message_handler()
async def get_weather(message: types.Message):
    
    # Википедие
    language = "ru"
    wikipedia.set_lang(language)
    
    if "Aexiss" in message.text:
        try:
            await message.reply(wikipedia.summary((message.text).replace("Aexiss", "").lstrip()))
        except wikipedia.exceptions.PageError:
            await message.reply("Я не смог это найти(")


    else:
        # Погода
        r = requests.get(

            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"

        )
        data = r.json()
        

        city = data["name"]
        cur_weather = data["main"]["temp"]
        
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        
        await message.reply(f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
                f"Ветер: {wind}м\с\n"
                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}")
            
    



if __name__ == "__main__":
    executor.start_polling(dp)
