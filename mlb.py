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
    text = "Temperatura: " + str(round(float(feeds[1]['field1']),1)) + " C\n"  \
        "Umidita': " + str(round(float(feeds[1]['field2']),1)) + " %\n" \
        "Dew Point: " + str(round(float(feeds[1]['field3']), 1)) + \
        " C\n" \
        "Pressione: " + str(round(float(feeds[1]['field4']), 1)) + \
        " hPa\n" \
        "Rain: " + str(round(float(feeds[1]['field7']), 1)) + \
        " mm\n" \
        "Prob. di nebbia (se <2.5): " + \
        str(round(float(feeds[1]['field1'])
            - float(feeds[1]['field3']), 1)) + " C"
    print(text)

    if msg['text'] == 'Meteo' or msg['text'] == 'meteo':
        bot.sendMessage(chat_id, text)

    # if content_type == 'text':
    #    bot.sendMessage(chat_id, text)


TOKEN = '*'    # token del bot

bot = telepot.Bot('TOKEN')  # da tenere nascosto per evitare leak
                            # eventualmente avvisat da GitGurdian
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
