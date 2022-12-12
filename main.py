from telethon import events, sync, TelegramClient
import os
import requests
import os.path

# Use the "BOT_TOKEN" and "API_ID" and "API_HASH" environment variables
# to get the API token and API credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Use the async context manager to run the client in async mode
async with TelegramClient("my_bot", API_ID, API_HASH) as client:
    # This method sends a message with instructions on how to use the bot
    async def help_message(event):
        help_text = "Send me a photo to colorize it!"
        await client.send_message(event.chat_id, help_text)

    # This method sends a welcome message to the user when they start the bot
    async def start_message(event):
        welcome_text = "Hi! I'm a bot that can colorize photos. Send me a photo to get started!"
        await client.send_message(event.chat_id, welcome_text)

    async def colorize_photo():
        url = 'https://playback.fm/colorize-photo'
        with open("image.jpg", "rb") as image_file:
            response = requests.post(
                url,
                files={"image": image_file},
                data={"xhr": "true"},
            )
        # Print the response from the server
        print(response.text)
        return response

    # Use the colorize_photo method to make a request to the
    # https://playback.fm/colorize-photo web service and colorize
    # the image in the file located at "image.jpg" when a user
    # sends a photo to the bot
    @client.on(events.NewMessage(pattern=".*", outgoing=False, incoming=True, func=lambda e: e.message.photo))
    async def handle_photo(event):
        message = event.message
        # Call the colorize_photo method to make the request to the server
        response = await colorize_photo()
        # Send the colorized image to the user
        await client.send_file(event.chat_id, response.content)
        # Delete the "image.jpg" file
        if os.path.exists("image.jpg"):
            os.remove("image.jpg")

    # Handle the "/start" and "/help" commands
    @client.on(events.NewMessage(pattern="/start"))
    async def handle_start(event):
        # Call the start_message method to send the welcome message
        await start_message(event)

    @client.on(events.NewMessage(pattern="/help"))
    async def handle_help(event):
        # Call the start_message method to send the welcome message
        await help_message(event)

client.run_until_disconnected()
