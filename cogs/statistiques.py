import discord
from cogs.affichage import couleur
from cogs.affichage import embed
from discord.ext import commands
from discord.utils import get

class Statistiques(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def stats(self, ctx):
        mute = get(ctx.guild.roles, name="Mute")


        message = self.embed(self.couleur.blueColor, "E.V.E - Statistiques", "Chargement du rapport détaillé de la situation...", self.couleur.blueImageEve)
        message.format.add_field(name="=== Statistiques membres ===", value="Voici toutes les informations relatives aux membres de votre serveur actuellement.", inline=False)
        message.format.add_field(name="Total :globe_with_meridians:", value=f"{sum(not member.bot for member in ctx.guild.members)} membre(s)")
        message.format.add_field(name="Connecté :green_circle:", value=f"{sum(member.status == discord.Status.online and not member.bot for member in ctx.guild.members)} membre(s)")
        message.format.add_field(name="Déconnecté :sleeping:", value=f"{sum(member.status == discord.Status.offline and not member.bot for member in ctx.guild.members)} membre(s)")
        message.format.add_field(name="Mute :face_with_symbols_over_mouth:", value=f"{sum(mute in member.roles for member in ctx.guild.members)} membre(s)")
        message.format.add_field(name="Absent :orange_circle:", value=f"{sum(member.status == discord.Status.idle and not member.bot for member in ctx.guild.members)} membre(s)")
        message.format.add_field(name="Ne pas déranger :no_entry:", value=f"{sum(member.status == discord.Status.do_not_disturb and not member.bot for member in ctx.guild.members)} membre(s)")

        message.format.add_field(name="=== Statistiques bots ===", value="fddf", inline=False)
        message.format.add_field(name="Total :globe_with_meridians:", value=f"{sum(member.bot for member in ctx.guild.members)} bot(s)")
        message.format.add_field(name="Connecté :green_circle:", value=f"{sum(member.status == discord.Status.online and member.bot for member in ctx.guild.members)} bot(s)")
        message.format.add_field(name="Déconnecté :sleeping:", value=f"{sum(member.status == discord.Status.offline and member.bot for member in ctx.guild.members)} bot(s)")

        message.format.add_field(name="=== Statistiques E.V.E", value="Vous trouverez ici toutes les informations en relation avec mes systèmes.", inline=False)
        message.format.add_field(name="Ping :arrows_counterclockwise:", value=f"{round(self.eve.latency * 1000)} ms", inline=False)
        if str(ctx.guild.me.nick) == "E.V.E - Emergency Protocol":
            message.format.add_field(name="Emergency Protocol Activated :beginner:", value="Attention, niveau de sécurité : Critique ! Mon protocole d'urgence est actif, la sécurité du serveur est désormais ma priorité.")
        else:
            message.format.add_field(name="Emergency Protocol Disabled :beginner:", value="Niveau de sécurité : Stable. Mon protocole d'urgence n'est pas actif.")

        await ctx.channel.send(content=None, embed=message.format)

def setup(eve):
    eve.add_cog(Statistiques(eve))