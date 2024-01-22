from os import getenv
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message as DiscordMessage
from openai import OpenAI
from datetime import datetime

import OpenAIManager as ai


# LOAD ENVIRONMENT VARIABLES
load_dotenv()
BOT_TOKEN: Final[str] = getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY: Final[str] = getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID: Final[str] = getenv("OPENAI_ASSISTANT_ID")


# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

openAI_client = OpenAI(api_key=OPENAI_API_KEY)
ai_assistant = ai.AssistantManager(openAI_client, OPENAI_ASSISTANT_ID)


# BOT STARTUP
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


@client.event
async def on_message(message: DiscordMessage) -> None:
    print(f"\n---{datetime.now()}---\nMessage from {message.author}:\n\t"
          + message.content)
    
    if message.author == client.user:
        return
    
    # if not "bot" in str(message.channel):
    #     print("Message channel does not contain \'bot\' in it. ")
    #     return
    
    if not message.content.startswith(client.user.mention):
        await message.channel.send("(Make sure to mention me if you want a response. Rules are rules.)")
        return
    
    
    print("------ Parsing the message.")
    parsed_message = ai.Message(str(message.content), str(message.channel))
    
    if "\messages" in str(message.content):
        thread_id = ai_assistant.threads.get_thread_id_local(parsed_message.thread_key)
        thread = ai_assistant.threads.get_thread_remote(thread_id)
        msg_history = ai_assistant.threads.get_messages_remote(thread)
        response = "\n\n".join([f"{i}: {msg}" for i, msg in enumerate(msg_history[:5])])
        await message.channel.send(response)
        return
    
    print("------ Sending the parsed message.")
    response = ai_assistant.send_message(parsed_message)    
    
    # Create a reply message formatted as a Discord reply box
    # reply_message = f"> **Original Message from {message.author.display_name}:**\n> {message.content}\n\n{response}"
    
    print("------ Awaiting opportunity to serve response to channel.")
    # await message.channel.send(reply_message)
    await message.reply(response)



def main() -> None: 
    client.run(token=BOT_TOKEN)


if __name__=="__main__":
    main()
