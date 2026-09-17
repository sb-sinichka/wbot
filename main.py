import telebot
import requests
import pyttsx3

engine = pyttsx3.init()

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def get_weather(city: str) -> str:
    url = f'https://wttr.in/{city}?format=%C+%t'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return 'Не удалось получить данные о погоде. Попробуйте позже.'


bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, который озвучивает прогноз погоды.')


@bot.message_handler(commands=['weather'])
def weather(message):
    words = message.text.split(maxsplit = 1)

    if len(words) < 2:
        bot.send_message(message.chat.id,'Пожалуйста, укажи город. Пример: /weather London')
        return
    
    city = words[1]
    w_info = get_weather(city)
    result = f'Погода в городе {city}: {w_info}'
    bot.send_message(message.chat.id, result)
    engine.save_to_file(result, "file.mp3")
    with open("file.mp3", "rb") as f:
        @bot.send_voice(message.chat.id, f)
    


bot.polling()