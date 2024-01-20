from os import getenv
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message as DiscordMessage
from openai import OpenAI

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
    print("Message detected.")
    
    if message.author == client.user:
        return
    
    if not "bot" in str(message.channel):
        print("Message channel does not contain \'bot\' in it. ")
        return
    
    parsed_message = ai.Message(message)
    response = ai_assistant.send_message(parsed_message)    
    await message.channel.send(response)



def main() -> None: 
    client.run(token=BOT_TOKEN)


if __name__=="__main__":
    main()
