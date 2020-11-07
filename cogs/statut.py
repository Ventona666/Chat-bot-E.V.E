import time
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from cogs.affichage import couleur
from cogs.affichage import embed

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