import discord
from dotenv import load_dotenv
import os

load_dotenv()

SECRET = "."
TOKEN = os.getenv("USER_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user and message.content == SECRET:
            await self.purge_messages([message.channel])

    async def purge_messages(self, channels):
        for channel in channels:
            print(f"Purging messages from: {channel}")

            with open("deleted.log", "a", encoding="utf-8") as msg_log:
                msg_log.write(f"Purging messages from: {channel}\n")

                try:
                    messages = []

                    async for msg in channel.history(limit=100):
                        if msg.author == self.user:
                            print(f"[{msg.created_at}] {msg.content}")
                            msg_log.write(f"[{msg.created_at}] {msg.content}\n")
                            messages.append(msg)

                    if messages:
                        await channel.delete_messages(messages)
                        msg_log.close()
                except Exception as e:
                    print(f"Can't purge messages: {e}")

client = MyClient(heartbeat_timeout=86400, guild_subscriptions=False)
client.run(TOKEN)