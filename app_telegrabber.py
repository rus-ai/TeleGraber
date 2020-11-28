
from telethon import TelegramClient, events
import datetime
import config
import logging

file_log = logging.FileHandler('telegrabber.log')
console_out = logging.StreamHandler()

# add filemode="w" to overwrite
# noinspection PyArgumentList
logging.basicConfig(handlers=[console_out, file_log],
                    format='[%(asctime)s | %(levelname)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

start_time = datetime.datetime.now()

stats = {"start_time": str(start_time),
         "uptime": 0,
         "text_events": 0,
         "media_events": 0,
         "album_events": 0,
         "spam_blocked": 0
         }

client = TelegramClient(config.app_name, config.api_id, config.api_hash)


logging.info("Telegram grabber")
logging.info("Channel to grab list: "+str(config.channels))
logging.info("Channel to post: "+config.my_channel_id)
logging.info("Stop words: "+str(config.stop_words))
logging.info("Work begin")




@client.on(events.NewMessage(chats=config.channels))
async def my_event_handler(event):
    logging.info("Channels event")
    logging.info(event.message)
    for word in config.stop_words:
        if word in event.message.text:
            logging.info("Spam post skipped")
            return
    if event.message.text:
        logging.info("Text event")
        await client.send_message(config.my_channel_id, event.message.text, link_preview=True)
        return
    if event.message.media:
        logging.info("Media event")
        await client.send_file(config.my_channel_id, file=event.message)
        return
    logging.info("Unhandled message type")


@client.on(events.Album(chats=config.channels))
async def handler(event):
    logging.info("Album event")
    await client.send_message(
        config.my_channel_id,
        file=event.messages,
        message=event.original_update.message.message,
    )


client.start()
client.run_until_disconnected()


# async def main():
#     # Now you can use all client methods listed below, like for example...
#     await client.send_message(config.my_channel_id, "test https://ya.ru", link_preview=True)
#
# with client:
#     client.loop.run_until_complete(main())
