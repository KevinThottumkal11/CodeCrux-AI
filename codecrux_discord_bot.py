"""
This script turns the CodeCruxGPT bot into a Discord bot that responds to user queries related to programming in real time.
The bot will respond to every message it receives in any server it is invited to.

Kevin Binu Thottumkal, Mohawk College, 15 November 2024
"""

import discord
from codecrux_bot import *

## MYClient Class Definition

class MyClient(discord.Client):
    """Represents the Discord bot client that listens for messages and interacts with users.
    This class extends the `discord.Client` class provided by the Discord API to define
    custom behaviors for the bot."""

    def __init__(self):
        """Constructor for MyClient class. Initializes the bot with default intents, which
        specify the bot's permissions and the events (reading messages) it listens for."""

        intents = discord.Intents.default()     # Default permissions
        intents.message_content = True          # reading messages
        super().__init__(intents=intents)       # Initialized with deafult intents

    async def on_ready(self):
        """Called when the bot has successfully logged in and is ready to start interacting.
        This method will print the bot's username to confirm successful login."""

        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object contains
        information about the message, including the author, channel, and content.
        The bot ignores its own messages to prevent infinite loops.
        If the message is from a user, it processes the user's message, understands the intent,
        generates a response using the Canada FAQ bot, and sends the response back to the same channel.

        The bot shuts down if the user input is goodbye"""

        # Ignores its own messages to prevent infinite loops.
        if message.author == self.user:
            return

        if self.user.mentioned_in(message) and message.content.strip().lower() == f"@{self.user.name} goodbye".lower():
            await message.channel.send("It was nice chatting with you! Take care! Shutting down...")
            await self.close()
            return

        # Responds only if the bot is mentioned
        if self.user.mentioned_in(message):
            global msg

            # Get the content of the message and process it through the Canada FAQ bot
            utterance = message.content     # message content



            # Bot shuts down if the user input is goodbye
            # if (utterance.strip().lower() == "goodbye"):
            #     await message.channel.send("It was nice chatting with you! Take care! Shutting down...")
            #     await self.close()
            # else:
            intent = understand(utterance)
            response = generate(intent, utterance)


            msg = message

            # send the response back to the channel
            # Bot was crashing when the len is greater than 2000
            if len(response) > 2000:
            # Split the response into chunks and send each chunk
                for i in range(0, len(response), 2000):
                    await message.channel.send(response[i:i + 2000])
            else:
            # Send the entire response if it's within the limit
                await message.channel.send(response)
            # await message.channel.send(response)

## Set up and log in
client = MyClient()

with open("bot_token.txt") as file:
    token = file.read()

## Run the bot using the token
client.run(token)