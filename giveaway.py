import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
import json
import random

def read_active_giveaways():
    try:
        with open("active_giveaways.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_active_giveaways(data):
    with open("active_giveaways.json", "w") as file:
        json.dump(data, file, indent=4)

def read_ended_giveaways():
    try:
        with open("ended_giveaways.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_ended_giveaways(data):
    with open("ended_giveaways.json", "w") as file:
        json.dump(data, file, indent=4)

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_giveaway.start()

    @app_commands.command(name="gcreate", description="Créer un giveaway.")
    @app_commands.default_permissions(administrator=True)
    async def gcreate(self, inter: discord.Interaction, reward: str, duration: str):
        unit = duration[-1]
        time = int(duration[:-1])

        if unit == "s":
            delay = time
        elif unit == "m":
            delay = time * 60
        elif unit == "h":
            delay = time * 3600
        else:
            await inter.response.send_message("Unité de temps invalide. Utilisez s, m, ou h.", ephemeral=True)
            return

        end_time = datetime.utcnow() + timedelta(seconds=delay)

        embed = discord.Embed(
            title="Giveaway!",
            description=f"Participez au giveaway pour **{reward}**! Réagissez avec 🎉 pour participer.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Durée", value=duration)
        embed.set_footer(text="Bonne chance!")
        embed.timestamp = end_time

        message = await inter.channel.send(embed=embed)
        await message.add_reaction("🎉")

        active_giveaways = read_active_giveaways()
        active_giveaways[str(message.id)] = {
            "guild_id": inter.guild.id,
            "channel_id": inter.channel.id,
            "reward": reward,
            "end_time": end_time.isoformat(),
        }
        write_active_giveaways(active_giveaways)
        await inter.response.send_message(f"Le giveaway pour **{reward}** a été créé avec succès!", ephemeral=True)

    @app_commands.command(name="greroll", description="Reroll the giveaway winner.")
    @app_commands.default_permissions(administrator=True)
    async def greroll(self, inter: discord.Interaction, message_id: str):
        ended_giveaways = read_ended_giveaways()
        giveaway = ended_giveaways.get(message_id)

        if not giveaway:
            await inter.response.send_message("Aucun giveaway trouvé avec cet ID.", ephemeral=True)
            return

        guild = self.client.get_guild(giveaway["guild_id"])
        channel = guild.get_channel(giveaway["channel_id"])
        message = await channel.fetch_message(int(message_id))

        users = []
        for reaction in message.reactions:
            if reaction.emoji == "🎉":
                async for user in reaction.users():
                    if not user.bot:
                        users.append(user)
                break

        if users:
            winner = random.choice(users)
            await channel.send(f"Félicitations, {winner.mention}! Vous avez gagné **{giveaway['reward']}** lors du reroll!")
            giveaway['winner'] = winner.mention
            write_ended_giveaways(ended_giveaways)
        else:
            await inter.response.send_message("Personne n'a participé au giveaway.", ephemeral=True)

    @tasks.loop(seconds=5)
    async def check_giveaway(self):
        now = datetime.utcnow()
        active_giveaways = read_active_giveaways()
        ended_giveaways = read_ended_giveaways()
        to_delete = []

        for message_id, giveaway in active_giveaways.items():
            end_time = datetime.fromisoformat(giveaway["end_time"])

            if now >= end_time:
                guild = self.client.get_guild(giveaway["guild_id"])
                channel = guild.get_channel(giveaway["channel_id"])
                message = await channel.fetch_message(int(message_id))
                
                users = []
                for reaction in message.reactions:
                    if reaction.emoji == "🎉":
                        async for user in reaction.users():
                            if not user.bot:
                                users.append(user)
                        break

                if users:
                    winner = random.choice(users)
                    await channel.send(f"Félicitations, {winner.mention}! Vous avez gagné **{giveaway['reward']}**!")

                    giveaway['winner'] = winner.mention
                    ended_giveaways[str(message.id)] = giveaway
                    write_ended_giveaways(ended_giveaways)
                else:
                    await channel.send("Personne n'a participé au giveaway.")

                to_delete.append(message_id)

        for message_id in to_delete:
            del active_giveaways[message_id]

        write_active_giveaways(active_giveaways)