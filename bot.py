import discord
from discord.ext import commands
import os
from general_commands import General
from help_command import Help


# CONSTANTS AND PARAMETERS
TOKEN = os.environ["DS_TOKEN"]
intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category='Non sorted commands')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('%'),
    case_insensitive=True,
    intents=intents,
    help_command=help_command
)
# Default help command is replaced with a more fancy one (check "help_command.py")
bot.remove_command("help")


# START
@bot.event
async def on_ready():
    await bot.add_cog(General(bot))
    await bot.add_cog(Help(bot))
    await bot.tree.sync()
    await bot.wait_until_ready()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


bot.run(TOKEN)
