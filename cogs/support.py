# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Send an invitation to contact support.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import discord
from discord.utils import find
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur


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
