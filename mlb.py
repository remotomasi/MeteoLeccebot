import time
import json
from urllib import request
import telepot
from telepot.loop import MessageLoop


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg)

    # immagazzina in una variabile la risposta dal GET response
    response = request.urlopen(
        'https://thingspeak.com/channels/145284/feeds.json?results=2')

    # preleva i dati json dalla richiesta
    data = response.read().decode('utf-8')

    # convertiamo la stringa in dizionario
    data_dict = json.loads(data)

    # separiamo i valori che ci interessano
    feeds = data_dict['feeds']

    # origin = msg
    # origin = msg.read().decode('utf-8')
    # data_msg = json.loads(msg)
    # dati = data_msg['field1']
    # print(msg['text'])

    # stampo i valori
    text = "La Temperatura è di: " + str(float(feeds[1]['field1'])) + " C\n"  \
        "L'Umidità è il: " + str(float(feeds[1]['field2'])) + " %\n" \
        "Il Dew Point è di: " + str(round(float(feeds[1]['field3']), 1)) + \
        " C\n" \
        "La Pressione è di: " + str(round(float(feeds[1]['field5']), 1)) + \
        " hPa\n" \
        "Prob. di nebbia (se <2.5): " + \
        str(round(float(feeds[1]['field1'])
            - float(feeds[1]['field3']), 1)) + " C"
    print(text)

    if msg['text'] == 'Meteo' or msg['text'] == 'meteo':
        bot.sendMessage(chat_id, text)

    # if content_type == 'text':
    #    bot.sendMessage(chat_id, text)


TOKEN = 'YOUR-TOKEN'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
