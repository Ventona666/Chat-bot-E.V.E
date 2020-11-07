import discord
from discord.utils import find
from cogs.affichage import couleur
from cogs.affichage import embed
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def support(self, ctx):
        message = embed.Embed(couleur.Couleur().blueColor, "E.V.E - Support", "Voici des informations qui pourraient correspondre à votre requête", couleur.Couleur().blueImageEve)
        message.format.add_field(name="Chargement des données...", value=f"Bienvenue {ctx.author.mention}, si vous souhaitez prendre contact avec mon support technique afin de signaler un bug, poser une question ou tout simplement pour remercier mon créateur, vous pouvez rejoindre notre serveur discord ci-dessous.")
        message.format.add_field(name="Voici le lien du support", value="https://discord.gg/FNn5U9N", inline=False)
        await ctx.channel.send(content=None, embed=message.format)


def setup(eve):
    eve.add_cog(Support(eve))