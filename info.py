import discord
from discord.ext import commands
from discord import app_commands



class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="ping", description="latence")
    async def ping(self, inter : discord.Interaction):
            latency = self.client.latency * 1000
            await inter.response.send_message(f"Ping : {latency:.2f} ms", ephemeral=False)

    @app_commands.command(name="serverinfo", description="Afficher les informations sur le serveur")
    async def serverinfo(self, inter: discord.Interaction):
        guild = inter.guild

        server_name = guild.name
        server_id = guild.id
        server_owner = guild.owner
        server_created_at = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        member_count = guild.member_count
        text_channels_count = len(guild.text_channels)
        voice_channels_count = len(guild.voice_channels)
        roles_count = len(guild.roles)

        embed = discord.Embed(title="Informations sur le serveur", color=discord.Color.blue())
        embed.add_field(name="Nom du serveur", value=server_name)
        embed.add_field(name="Identifiant du serveur", value=server_id)
        embed.add_field(name="Propriétaire", value=server_owner.mention)
        embed.add_field(name="Créé le", value=server_created_at)
        embed.add_field(name="Membres", value=member_count)
        embed.add_field(name="Salons textuels", value=text_channels_count)
        embed.add_field(name="Salons vocaux", value=voice_channels_count)
        embed.add_field(name="Rôles", value=roles_count)

        await inter.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="userinfo", description="Afficher les informations sur un utilisateur")
    async def userinfo(self, inter: discord.Interaction, member: discord.User = None):
        if member is None:
            member = inter.user

        username = member.name
        user_id = member.id
        user_created_at = member.created_at.strftime("%d/%m/%Y %H:%M:%S")
        is_booster = bool(member.premium_since)
        join_timestamp = f"<t:{int(member.joined_at.timestamp())}>"

        highest_role = member.top_role.name if member.top_role else "Aucun rôle"

        embed = discord.Embed(title="Informations sur l'utilisateur", color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Nom d'utilisateur", value=username)
        embed.add_field(name="Identifiant de l'utilisateur", value=user_id)
        embed.add_field(name="Créé le", value=user_created_at)
        embed.add_field(name="Membre Booster", value=is_booster)
        embed.add_field(name="Date d'arrivée", value=join_timestamp)
        embed.add_field(name="Rôle le plus haut", value=highest_role)

        await inter.response.send_message(embed=embed, ephemeral=False)
    
    @app_commands.command(name="botinfo", description="Afficher les informations sur le bot")
    async def botinfo(self, inter: discord.Interaction):
        bot_name = self.client.user.name
        bot_id = self.client.user.id
        bot_created_at = self.client.user.created_at.strftime("%d/%m/%Y %H:%M:%S")
        bot_owner = self.client.get_user(767412412731097108)
        bot_dead = await self.client.fetch_user(767412412731097108)
        bot_avatar = self.client.user.avatar

        embed = discord.Embed(title="Informations sur le bot", color=discord.Color.blue())
        embed.set_thumbnail(url=bot_avatar)
        embed.add_field(name="Nom du bot", value=bot_name)
        embed.add_field(name="Identifiant du bot", value=bot_id)
        embed.add_field(name="Créé le", value=bot_created_at)
        embed.add_field(name="Propriétaire du bot", value=bot_owner.name) 
        embed.add_field(name="Développeur", value=f"{bot_dead.name}")  

        await inter.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="avatar", description="Afficher l'avatar d'un utilisateur")
    async def avatar(self, inter: discord.Interaction, member: discord.User = None):
        if member is None:
            member = inter.user

        avatar_url = member.avatar

        embed = discord.Embed(title=f"Avatar de {member.name}", color=discord.Color.blue())
        embed.set_image(url=avatar_url)
        embed.description = f"Lien de l'avatar : <{avatar_url}>"

        await inter.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="membercount", description="Afficher le nombre de membres sur le serveur")
    async def membercount(self, inter: discord.Interaction):
        guild = inter.guild
        member_count = guild.member_count
    
        embed = discord.Embed(title="Nombre de membres sur le serveur", color=discord.Color.blue())
        embed.add_field(name="Membres", value=str(member_count))
    
        await inter.response.send_message(embed=embed, ephemeral=False)