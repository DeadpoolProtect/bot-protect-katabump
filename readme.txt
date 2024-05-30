Salut à vous, chers utilisateurs de ce code,

Merci de prendre soin de ce code. C'est le plus grand code que j'ai pu faire, haha j'abuse un peu, mais en tout cas, pour la liste blanche, ça a été le plus compliqué.

Bref, je le donne gratuitement et en open source, bien sûr.

Je vais vous mettre des codes ci-dessous si vous souhaitez changer des trucs 😉

Psst, voici un endroit pour héberger le bot : https://katabump.com/host

(Je compte faire des mises à jour sur ce code, donc restez connectés et n'oubliez pas de mettre une étoile sur le projet, ça ne coûte rien, merci à vous ♥)

Code pour envoyer un système de bienvenue et donner un rôle automatiquement
Tu vas dans le main.py et tu mets ce code :

@client.event
async def on_member_join(member):
    guild = member.guild
    channel_id = 1216311573337870427
    channel = guild.get_channel(channel_id)
    if channel is not None:
        member_count = guild.member_count
        message = f"> Bienvenue {member.mention} sur **KataBump Protect**. Nous sommes actuellement **{member_count}** membres sur le discord."
        await channel.send(message)
    role_id = 1216311571773394994
    role = discord.utils.get(guild.roles, id=role_id)
    if role is not None:
        await member.add_roles(role)

// info: channel_id = le canal où le bot va envoyer le message et role_id = l'ID du rôle que l'utilisateur va recevoir en rejoignant le discord.


Tutoriel simple pour désactiver le fichier level.py

1. tu va dans le fichier main.py

Recherchez la ligne import level.
Supprimez cette ligne.
Recherchez la ligne await client.add_cog(level.Level(client)).
Supprimez cette ligne également.
2. Suppression du fichier level.py

Supprimez le fichier level.py si vous n'en avez plus besoin.