import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta, timezone

def load_logs_config():
    if os.path.exists("logs.json"):
        with open("logs.json", "r") as file:
            return json.load(file)
    return {
        "logs_category_id": 0,
        "logs_message_id": 0,
        "logs_ban_id": 0,
        "logs_unban_id": 0,
        "logs_voice_id": 0 
    }



def save_logs_config(config):
    with open("logs.json", "w") as file:
        json.dump(config, file)


class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name="setup_logs", description="Configurer les canaux de logs")
    @app_commands.default_permissions(administrator=True)
    async def setup_logs(self, inter: discord.Interaction):
        guild = inter.guild
        logs_category = await guild.create_category("📁・Espace logs")

        logs_message = await guild.create_text_channel("📁・logs-message", category=logs_category)
        logs_ban = await guild.create_text_channel("📁・logs-ban", category=logs_category)
        logs_unban = await guild.create_text_channel("📁・logs-unban", category=logs_category)
        logs_voice = await guild.create_text_channel("📁・logs-vocal", category=logs_category)

        config = load_logs_config()
        config["logs_category_id"] = logs_category.id
        config["logs_message_id"] = logs_message.id
        config["logs_ban_id"] = logs_ban.id
        config["logs_unban_id"] = logs_unban.id
        config["logs_voice_id"] = logs_voice.id
        save_logs_config(config)

        await logs_category.set_permissions(guild.default_role, read_messages=False)
        await logs_message.set_permissions(guild.default_role, read_messages=False)
        await logs_ban.set_permissions(guild.default_role, read_messages=False)
        await logs_unban.set_permissions(guild.default_role, read_messages=False)
        await logs_voice.set_permissions(guild.default_role, read_messages=False)

        await inter.response.send_message("Les canaux de logs ont été configurés !", ephemeral=True)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        config = load_logs_config()
        logs_channel_id = config.get("logs_message_id", 0)

        if logs_channel_id != 0 and before.content != after.content:
            logs_channel = self.client.get_channel(logs_channel_id)
            if logs_channel:
                embed = discord.Embed(title="Message édité", color=discord.Color.blue())
                embed.add_field(name="Auteur", value=before.author.mention, inline=False)
                embed.add_field(name="Avant", value=before.content, inline=False)
                embed.add_field(name="Après", value=after.content, inline=False)
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        config = load_logs_config()
        logs_channel_id = config.get("logs_message_id", 0)

        if logs_channel_id != 0:
            logs_channel = self.client.get_channel(logs_channel_id)
            if logs_channel:
                embed = discord.Embed(title="Message supprimé", color=discord.Color.blue())
                embed.add_field(name="Auteur", value=message.author.mention, inline=False)
                embed.add_field(name="Contenu", value=message.content, inline=False)
                await logs_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        config = load_logs_config()
        logs_channel_id = config.get("logs_ban_id", 0)

        if logs_channel_id != 0:
            logs_channel = self.client.get_channel(logs_channel_id)
            if logs_channel:
                entry = None
                async for e in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                    if e.target == user:
                        entry = e
                        break
                    
                embed = discord.Embed(title="Membre banni", color=discord.Color.blue())
                embed.add_field(name="Membre", value=user.mention, inline=False)
                if entry:
                    embed.add_field(name="Banni par", value=entry.user.mention, inline=False)
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        config = load_logs_config()
        logs_channel_id = config.get("logs_unban_id", 0)

        if logs_channel_id != 0:
            logs_channel = self.client.get_channel(logs_channel_id)
            if logs_channel:
                entry = None
                async for e in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
                    if e.target == user:
                        entry = e
                        break
                    
                embed = discord.Embed(title="Membre débanni", color=discord.Color.blue())
                embed.add_field(name="Membre", value=user.mention, inline=False)
                if entry:
                    embed.add_field(name="Débanni par", value=entry.user.mention, inline=False)
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        config = load_logs_config()
        logs_channel_id = config.get("logs_voice_id", 0)

        if logs_channel_id != 0 and before.channel != after.channel:
            logs_channel = self.client.get_channel(logs_channel_id)
            if logs_channel:
                if before.channel:
                    embed = discord.Embed(title="Membre a quitté un salon vocal", color=discord.Color.blue())
                    embed.add_field(name="Membre", value=member.mention, inline=False)
                    embed.add_field(name="Salon avant", value=before.channel.name, inline=False)
                    await logs_channel.send(embed=embed)
                
                if after.channel:
                    embed = discord.Embed(title="Membre a rejoint un salon vocal", color=discord.Color.green())
                    embed.add_field(name="Membre", value=member.mention, inline=False)
                    embed.add_field(name="Salon après", value=after.channel.name, inline=False)
                    await logs_channel.send(embed=embed)