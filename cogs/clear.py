from discord.ext import commands
from discord.utils import get
import discord
from cogs.affichage import couleur
from cogs.affichage import embed

class Clear(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def clear(self, ctx, nombre):
        if get(ctx.guild.roles, name="Master") in ctx.author.roles:
            await ctx.channel.purge(limit=int(nombre)+1)
        else:
            message = self.embed(self.couleur.redColor, "Erreur E.V.E - Commande refusée", "Vous n'êtes pas un superviseur", self.couleur.redImageEve)
            message.format.add_field(name="Explication", value="Vous n'êtes pas un superviseur, vous n'avez donc pas accès à cette commande. ", inline=False)
            await ctx.channel.send(content=None, embed=message.format)

def setup(eve):
    eve.add_cog(Clear(eve))