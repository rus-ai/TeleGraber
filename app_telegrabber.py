from telethon import TelegramClient, events
import config
import asyncio

client = TelegramClient(config.app_name, config.api_id, config.api_hash)

print("Work begin")

@client.on(events.NewMessage(chats=config.channels))
async def my_event_handler(event):
    if event.message.text:
        print("Message event")
        await client.send_message(config.my_channel_id, event.message)
    if event.message.media:
        print("Media event")
        await client.send_file(config.my_channel_id, file=event.message)

@client.on(events.Album(chats=config.channels))
async def handler(event):
    await client.send_message(
        config.my_channel_id,
        file=event.messages,
        message=event.original_update.message.message,
    )


client.start()
client.run_until_disconnected()
