# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Status manager.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import time
import discord
from discord.utils import get
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur
from discord.ext.commands import Bot


class Statut(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.Cog.listener()
    async def on_ready(self):
        """ Change le statut discord et préviens lorsque Eve est prête à être utilisée """

        await self.eve.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.eve.guilds)} serveurs"))
        print(f"Procédure de démarrage enclenchée le {time.strftime('%c', time.localtime(time.time()))}. E.V.E démarrée avec succès !")


def setup(eve):
    eve.add_cog(Statut(eve))
