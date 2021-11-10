import discord 
from discord.ext import commands
import config

cogs = ["cogs.poems.poem", "cogs.todo.todolist"]
intents = discord.Intents().all()
client = commands.Bot(command_prefix=config.CMD_PREFIX, help_command=None, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("No rebanho do Mestre Caeiro"))
    print("Logged in as {}".format(client.user))

for extension in cogs:
    client.load_extension(extension)

client.run(config.BOT_TOKEN)