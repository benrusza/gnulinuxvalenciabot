import os
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN_TELEGRAM')


def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='tribe-events-widget-events-list__events')
        if div:
            events = []
            event_titles = div.find_all('h3', class_='tribe-events-widget-events-list__event-title')
            for title in event_titles:
                a_tag = title.find('a')
                if a_tag:
                    events.append({
                        'title': a_tag.text.strip(),
                        'link': a_tag['href']
                    })
            text = str(events).replace("}, {","\n").replace("{","").replace("[","").replace("]","").replace("}","").replace(", ","\n")
            #events = events.replace("{","").replace("[","").replace("]","").replace("}","")
            print("text: "+text)
            return text
            print("Div not found")
    except Exception as e:
        print(f"An error occurred: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Comandaments:\n/proxim_event')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def next_event(update: Update,context : ContextTypes.DEFAULT_TYPE):
    url = "https://gnulinuxvalencia.org"
    nextevent = extract_data(url)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=nextevent)

async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='https://github.com/benrusza/gnulinuxvalenciabot')


def main():
    application = ApplicationBuilder().token(API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    next_event_handler = CommandHandler(['next_event','proximo_evento','proxim_event'],next_event)
    application.add_handler(next_event_handler)

    get_source_handler = CommandHandler(['source','font'],get_source)
    application.add_handler(get_source_handler)

    #echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    #application.add_handler(echo_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
