from telethon import events, sync, TelegramClient
import os
import requests
import os.path

# Use the "BOT_TOKEN" and "API_ID" and "API_HASH" environment variables
# to get the API token and API credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("my_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# This method sends a message with instructions on how to use the bot
def help_message(event):
    help_text = "Send me a photo to colorize it!"
    client.send_message(event.chat_id, help_text)

# This method sends a welcome message to the user when they start the bot
def start_message(event):
    welcome_text = "Hi! I'm a bot that can colorize photos. Send me a photo to get started!"
    client.send_message(event.chat_id, welcome_text)

def colorize_photo():
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
def handle_photo(event):
    message = event.message
    # Call the colorize_photo method to make the request to the server
    response = colorize_photo()
    # Send the colorized image to the user
    client.send_file(event.chat_id, response.content)
    # Delete the "image.jpg" file
    if os.path.exists("image.jpg"):
        os.remove("image.jpg")

# Handle the "/start" and "/help" commands
@client.on(events.NewMessage(pattern="/start"))
def handle_start(event):
    # Call the start_message method to send the welcome message
    start_message(event)

@client.on(events.NewMessage(pattern="/help"))
def handle_help(event):
    # Call the help_message method to send the help message
    help_message(event)

client.run_until_disconnected()
