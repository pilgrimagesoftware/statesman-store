__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
discord
- Discord controller
"""


# from flask import current_app
# import os
# import discord
# # import threading
# # import asyncio
# import multiprocessing


# class DiscordClient(discord.Client):
#     async def on_ready(self):
#         current_app.logger.info('Logged on as %s', self.user)

#     async def on_message(self, message):
#         current_app.logger.info("message: %s", message)

#         # don't respond to ourselves
#         if message.author == self.user:
#             return

#         if message.content == 'ping':
#             await message.channel.send('pong')


# async def run_discord_client():
#     client = DiscordClient()
#     print("client:", client)
#     await client.start()
# # #     print("Starting Discord client...")
# # #     client.run(os.environ['DISCORD_TOKEN'])

# # discord_task = asyncio.create_task(run_discord_client)
# # # thread = threading.Thread(target=run_discord_client)
# # # thread.start()

# discord_proc = multiprocessing.Process(target=run_discord_client, daemon=True)
# discord_proc.start()
