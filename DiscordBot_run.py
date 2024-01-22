from os import getenv
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message as DiscordMessage
from openai import OpenAI
from datetime import datetime
from discord.ext import commands
from discord import errors

import OpenAIManager as ai


# LOAD ENVIRONMENT VARIABLES
load_dotenv()
BOT_TOKEN: Final[str] = getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY: Final[str] = getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID: Final[str] = getenv("OPENAI_ASSISTANT_ID")


# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
# bot: Client = Client(intents=intents)

# Use commands.Bot instead of discord.Client
bot = commands.Bot(command_prefix='!', intents=intents)

openAI_client = OpenAI(api_key=OPENAI_API_KEY)
ai_assistant = ai.AssistantManager(openAI_client, OPENAI_ASSISTANT_ID)


# BOT STARTUP
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')


@bot.event
async def on_message(message: DiscordMessage) -> None:
    
    print(f"\n---{datetime.now()}---\nMessage from {message.author}:\n\t"
          + message.content)
        

    if message.author == bot.user:
        return
    
    if not "bot" in str(message.channel) and not message.content.startswith(bot.user.mention):
        print("Channel does not contain \'bot\' in it and bot not mentioned.")
        return
    

    print("------ Parsing the message.")    
    parsed_messaged: ai.Message = None

    if message.content.startswith(bot.user.mention):
        message.content = message.content[len(bot.user.mention)+1:]
        parsed_message = ai.Message(str(message.content), str(message.author))
    
    if "bot" in str(message.channel):
        parsed_message = ai.Message(str(message.content), str(message.channel))
    

    print("------ Handling commands.")   
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return
    
    
    print("------ Sending the parsed message.")
    response = ai_assistant.send_message(parsed_message)

    
    print("------ Awaiting opportunity to serve response to channel.")
    # await message.channel.send(reply_message)
    await message.reply(response)


# 
@bot.command(name="messages")
async def fetch_thread_message_history(ctx, num_messages: int = 5):
    thread_key = ""
    is_reply = False
    if ctx.message.content.startswith(bot.user.mention):
        thread_key = str(ctx.author)
        is_reply = True
    else:
        thread_key = str(ctx.channel)

    thread_id = ai_assistant.threads.get_thread_id_local(thread_key)
    thread = ai_assistant.threads.get_thread_remote(thread_id)
    msg_history = ai_assistant.threads.get_messages_remote(thread)

    response = ""
    if num_messages > len(msg_history):
        response = f"(Message history is only {len(msg_history)} messages long.)\n\n"
        num_messages = len(msg_history)
    response += "\n\n".join([f"{i}: {msg}" for i, msg in enumerate(msg_history[:num_messages])])
    
    try:
        if len(response) <= 2000:
            if is_reply:
                await ctx.reply(response)
            else:
                await ctx.channel.send(response)
        else:
            # Split the message into chunks of 2000 characters
            for i in range(0, len(response), 2000):
                chunk = response[i:i+2000]
                if is_reply:
                    await ctx.reply(chunk)
                else:
                    await ctx.channel.send(chunk)

    except errors.HTTPException as e:
        # Handle the exception (e.g., log it, notify the user, etc.)
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while processing your request.")



def main() -> None: 
    bot.run(token=BOT_TOKEN)


if __name__=="__main__":
    main()
