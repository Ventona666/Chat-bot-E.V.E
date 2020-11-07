# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Simple timer.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import time
import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur


class Timer(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def chrono(self, ctx, duration):
        """ Fonction déclenchant un minuteur d'une durée définie par l'utilisateur """

        start = self.embed(self.couleur.blueColor, f"E.V.E - Minuteur de {duration} minute(s) déclenché", f"Initialisation du processus, durée du minuteur définie sur {duration} minute(s). Je vous préviendrai une fois que le minuteur sera terminé.", self.couleur.blueImageEve)
        await ctx.author.send(content=None, embed=start.format)

        await asyncio.sleep(int(duration) * 60)

        end = self.embed(self.couleur.blueColor, f"E.V.E - Fin du minuteur de {duration} minute(s)", f"Je vous informe que le minuteur est arrivé à son terme.", self.couleur.blueImageEve)
        await ctx.author.send(content=None, embed=end.format)

def setup(eve):
    eve.add_cog(Timer(eve))
