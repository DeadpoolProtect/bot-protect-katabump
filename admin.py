import discord
from discord.ext import commands
from discord import app_commands
import json
import os
lock_file = "lock.json"


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="roleall", description="Attribuer un rôle à tous les membres du serveur")
    @app_commands.default_permissions(administrator=True)
    async def roleall(self, inter: discord.Interaction, role: discord.Role):
        guild = inter.guild

        for member in guild.members:
            await member.add_roles(role)

        await inter.response.send_message("Le rôle a été attribué à tous les membres du serveur.", ephemeral=False)

    
    @app_commands.command(name="ban", description="Bannir un membre du serveur")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        guild = inter.guild

        if not guild.me.guild_permissions.ban_members:
            await inter.response.send_message("Je n'ai pas les permissions nécessaires pour bannir des membres.", ephemeral=True)
            return

        if member == guild.owner:
            await inter.response.send_message("Vous ne pouvez pas bannir le propriétaire du serveur.", ephemeral=True)
            return

        await member.ban(reason=reason)
        await inter.response.send_message(f"{member.name} a été banni du serveur.", ephemeral=False)


    @app_commands.command(name="kick", description="Kick un membre du serveur")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        guild = inter.guild

        if not guild.me.guild_permissions.kick_members:
            await inter.response.send_message("Je n'ai pas les permissions nécessaires pour kick des membres.", ephemeral=True)
            return

        if member == guild.owner:
            await inter.response.send_message("Vous ne pouvez pas kick le propriétaire du serveur.", ephemeral=True)
            return

        await member.kick(reason=reason)
        await inter.response.send_message(f"{member.name} a été kick du serveur.", ephemeral=False)


    @app_commands.command(name="unban", description="Débannir un membre du serveur")
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, inter: discord.Interaction, user_id: int, reason: str = None):
        guild = inter.guild

        if not guild.me.guild_permissions.ban_members:
            await inter.response.send_message("Je n'ai pas les permissions nécessaires pour débannir des membres.", ephemeral=True)
            return

        banned_users = await guild.bans()

        for ban_entry in banned_users:
            if ban_entry.user.id == user_id:
                await guild.unban(ban_entry.user, reason=reason)
                await inter.response.send_message(f"Le membre avec l'ID {user_id} a été débanni du serveur.", ephemeral=False)
                return

        await inter.response.send_message(f"Aucun membre banni avec l'ID {user_id} n'a été trouvé sur le serveur.", ephemeral=False)

    
    @app_commands.command(name="clear", description="Supprimer un nombre de messages dans le canal")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, inter: discord.Interaction, amount: int):
        if amount <= 0 or amount > 100:
            await inter.response.send_message("Le nombre de messages à supprimer doit être compris entre 1 et 100.", ephemeral=True)
            return
    
        try:
            deleted = await inter.channel.purge(limit=amount + 1)
            await inter.response.send_message(f"{len(deleted) - 1} messages ont été supprimés.", ephemeral=True)
        except discord.Forbidden:
            await inter.response.send_message("Je n'ai pas les permissions nécessaires pour supprimer des messages.", ephemeral=True)
        except discord.HTTPException:
            await inter.response.send_message("Une erreur s'est produite lors de la suppression des messages.", ephemeral=True)


    @app_commands.command(name="lock", description="Bloquer un salon")
    @app_commands.default_permissions(manage_channels=True)
    async def lock(self, inter: discord.Interaction):
        channel = inter.channel
        channel_id = channel.id

        if os.path.exists("lock.json"):
            with open("lock.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        if str(channel_id) in data:
            await inter.response.send_message("Ce salon est déjà verrouillé.", ephemeral=True)
            return
        
        await channel.set_permissions(channel.guild.default_role, send_messages=False)

        data[str(channel_id)] = True

        with open("lock.json", "w") as file:
            json.dump(data, file)

        await inter.response.send_message("Le salon a été verrouillé avec succès.", ephemeral=True)

    @app_commands.command(name="unlock", description="Débloquer un salon")
    @app_commands.default_permissions(manage_channels=True)
    async def unlock(self, inter: discord.Interaction):
        channel = inter.channel
        channel_id = channel.id

        if os.path.exists("lock.json"):
            with open("lock.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        if str(channel_id) not in data:
            await inter.response.send_message("Ce salon n'est pas verrouillé.", ephemeral=True)
            return

        await channel.set_permissions(channel.guild.default_role, send_messages=True)

        del data[str(channel_id)]

        with open("lock.json", "w") as file:
            json.dump(data, file)

        await inter.response.send_message("Le salon a été déverrouillé avec succès.", ephemeral=True)