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

launch_time = datetime.datetime.now()


class StatsClass(object):
    def __init__(self):
        self.start_time = str(launch_time)
        self.uptime = str(datetime.datetime.now() - launch_time)
        self.text_events = 0
        self.media_events = 0
        self.album_events = 0
        self.admin_events = 0
        self.spam_blocked = 0

    def increase(self, param):
        if param in self.__dict__:
            self.__setattr__(param, self.__getattribute__(param)+1)

    def update(self):
        self.uptime = str(datetime.datetime.now() - launch_time)

    def __str__(self):
        self.update()
        return str(self.__dict__)


stats = StatsClass()

client = TelegramClient(config.app_name, config.api_id, config.api_hash)

logging.info("Telegram grabber")
logging.info("Channel to grab list: " + str(config.channels))
logging.info("Channel to post: " + config.my_channel_id)
logging.info("Stop words: " + str(config.stop_words))
logging.info("Work begin")


@client.on(events.NewMessage(chats=config.admins))
async def my_admin_event_handler(event):
    stats.increase("admin_events")
    logging.info("Admin command received")
    command = str(event.message.text).upper()
    if "STATUS" in command:
        logging.info("Admin command received STATUS")
        await client.send_message(event.message.peer_id, str(stats), link_preview=False)
        return
    logging.info("Unknown admin command")


@client.on(events.NewMessage(chats=config.channels))
async def my_event_handler(event):
    logging.info("Channels event")
    logging.info(str(event.message))
    for word in config.stop_words:
        if word in event.message.text:
            stats.increase("spam_blocked")
            logging.info("Spam post skipped")
            return
    if event.message.text:
        logging.info("Text event")
        stats.increase("text_events")
        await client.send_message(config.my_channel_id, event.message.text, link_preview=True)
        return
    if event.message.media:
        stats.increase("media_events")
        logging.info("Media event")
        await client.send_file(config.my_channel_id, file=event.message)
        return
    logging.info("Unhandled message type")


@client.on(events.Album(chats=config.channels))
async def handler(event):
    stats.increase("album_events")
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
