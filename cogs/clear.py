# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Clear function to delete message on discord.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import discord
from discord.utils import get
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur


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
