import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta, timezone



class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="level", description="Afficher le niveau d'un utilisateur")
    async def level(self, inter: discord.Interaction, member: discord.User = None):
        if member is None:
            member = inter.user

        if os.path.exists("level.json"):
            with open("level.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        if str(member.id) in data:
            level = data[str(member.id)]["level"]
            xp = data[str(member.id)]["xp"]
        else:
            level = 0
            xp = 0

        embed = discord.Embed(title="Niveau", color=discord.Color.red())
        embed.add_field(name="Utilisateur", value=member.mention)
        embed.add_field(name="Niveau", value=level)
        embed.add_field(name="XP", value=xp)

        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if os.path.exists("level.json"):
            with open("level.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        user_id = str(message.author.id)
        if user_id not in data:
            data[user_id] = {
                "level": 0,
                "xp": 0
            }

        data[user_id]["xp"] += 1

        xp_needed = data[user_id]["level"] * 10 + 10
        if data[user_id]["xp"] >= xp_needed:
            data[user_id]["level"] += 1
            data[user_id]["xp"] = 0

            level_up_message = f"{message.author.mention} a atteint le niveau {data[user_id]['level']} !"
            await message.channel.send(level_up_message)

        with open("level.json", "w") as file:
            json.dump(data, file)

        await self.client.process_commands(message)