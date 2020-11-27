from telethon import TelegramClient, events
import config

client = TelegramClient(config.app_name, config.api_id, config.api_hash)

print("Telegram grabber")
print("Channel to grab list", config.channels)
print("Channel to post", config.my_channel_id)
print("Stop words", config.stop_words)
print("Work begin")



@client.on(events.NewMessage(chats=config.channels))
async def my_event_handler(event):
    print(event.message)
    for word in config.stop_words:
        if word in event.message.text:
            print("Spam post skipped")
            return
    if event.message.text:
        print("Text event")
        await client.send_message(config.my_channel_id, event.message)
        return
    if event.message.media:
        print("Media event")
        await client.send_file(config.my_channel_id, file=event.message)
        return
    print("Unhandled message type")


@client.on(events.Album(chats=config.channels))
async def handler(event):
    print("Album event")
    await client.send_message(
        config.my_channel_id,
        file=event.messages,
        message=event.original_update.message.message,
    )


client.start()
client.run_until_disconnected()
