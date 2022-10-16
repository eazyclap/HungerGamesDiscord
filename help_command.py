import discord
from discord.ext import commands
from discord.errors import Forbidden

"""
Original concept by Jared Newsom (AKA Jared M.F.)
Rewritten and optimized by github.com/nonchris
This version has been modified by me!
Original github link:
https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2
"""


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        aliases=["hlp", "aiuto", "aiut", "wtf"],
        help="\tHelp command! Come on it's in the name!"
    )
    async def help(self, ctx, *, module=None):
        """
        Shows all modules of that bot
        """

        # Variables to make the cog functional
        prefix = "%"
        version = "1.0"

        # Setting owner name
        owner_name = "eazyclap#1202"

        # Checks if cog parameter was given
        # If not: sending all modules and commands not associated with a cog
        if module is None:
            try:
                owner = ctx.guild.owner.mention

            except AttributeError:
                owner = owner_name

            # Starting to build embed
            emb = discord.Embed(title='Modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` or `/help <module>` to gain more information about that module '
                                            f':ice_cube:\n')

            # Iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # Adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # Integrating trough uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # If cog not in a cog
                # Listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # Adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # Setting information about author
            emb.add_field(name="About", value=f"This embed was originally developed by Chriѕ#0001, based on discord.py.\n\
                                    This version of it is maintained by {owner}\n")
            emb.set_footer(text=f"Bot is running {version}")

        # Block called when one cog-name is given
        # Trying to find matching cog and it's commands
        else:
            # Iterating trough cogs
            for cog in self.bot.cogs:
                # Check if cog is the matching one
                if cog.lower() == module.lower():

                    # Making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    # Getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # If cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # Found cog - breaking loop
                    break

            # If input not found
            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{module}` before :scream:",
                                    color=discord.Color.orange())

        # Sending reply embed using our own function defined above
        await send_embed(ctx, emb)
