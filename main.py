import discord
from discord import app_commands
from discord.ext import commands, tasks
import info
import admin
import help 
import level
import logs
import wl
import blacklist
import asyncio
import giveaway
client = commands.Bot(
  command_prefix='+', 
  case_insensitive=False,
  description=None,
  intents=discord.Intents.all(),
)


@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


async def main():
    try:
        await client.add_cog(info.Info(client))
        await client.add_cog(help.Help(client))
        await client.add_cog(admin.Admin(client))
        await client.add_cog(level.Level(client))
        await client.add_cog(logs.Logs(client))
        await client.add_cog(wl.Wl(client))
        await client.add_cog(blacklist.Blacklist(client))
        await client.add_cog(giveaway.Giveaway(client))
        await client.start("tontoken")
    except Exception as e:
        print(e)


discord.utils.setup_logging()
asyncio.run(main())