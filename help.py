import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="Affiche la liste des commandes du bot.")
    async def help(self, inter: discord.Interaction):
        categories_and_commands = {
            "wrench: Info": ["userinfo", "help", "serverinfo", "botinfo", "ping", "membercount"],
            "hammer: Administration ": ["ban", "unban", "kick", "clear", "roleall", "lock", "unlock", "setup_logs", "giveaway"],
        }

        embed = discord.Embed(
            title="Liste des commandes de KataBump Protect",
            description="Utilisez notre préfixe `/` pour utiliser une commande.",
            color=discord.Color.purple()
        )

        for category, commands_list in categories_and_commands.items():
            commands_text = " ".join([f"`{command}`" for command in commands_list])
            embed.add_field(name=f":{category}:", value=commands_text, inline=False)

        await inter.response.send_message(embed=embed, ephemeral=False)
