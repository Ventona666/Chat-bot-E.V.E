import discord
from cogs.affichage import couleur
from cogs.affichage import embed
from discord.ext import commands

class Erreur(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.Cog.listener()
    async def on_command_error(self, channel, error):
        """ Gestion des erreurs liées à une commande mal utilisée, par exemple le manque d'un paramètre. """

        if isinstance(error, commands.MissingRequiredArgument):
            message = self.embed(self.couleur.redColor, "E.V.E - Argument manquant", "Erreur liée à la commande utilisée", self.couleur.redImageEve)
            message.format.add_field(name="Chargement de l'erreur", value="Excusez-moi, cette commande nécessite un ou plusieurs arguments. Je vous invite à taper !aide pour comprendre le fonctionnement de cette commande.")
            await channel.send(content=None, embed=message.format)

def setup(eve):
    eve.add_cog(Erreur(eve))