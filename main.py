import telebot
import requests


TOKEN = "BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Kinopoisk bot! Please enter the name of a movie or TV show you want to search for.")


@bot.message_handler(func=lambda message: True)
def search_movie(message):
    query = message.text
    url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={query}'
    headers = {'X-API-KEY': "API_TOKEN"}
    response = requests.get(url, headers=headers).json()
    reply = ""
    try:
        response['films']
        film = response['films'][0]
        title = film['nameRu']
        try:
            title += f"\n{film['nameEn']}"
        except Exception:
            pass

        year = film['year']
        rating = film['rating']
        description = film['description']
        reply = f"{title}\n\year: {year}\nRating: {rating}\n\n{description}"
    except Exception:
        reply = "Sorry, I couldn't find any movies or TV shows with that name."
    
    bot.reply_to(message=message, text=reply)


bot.polling()
