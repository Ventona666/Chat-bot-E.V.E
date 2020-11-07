import discord
from discord.ext import commands
from discord.utils import get


class Embed():
    """ Classe définissant l'embed, à savoir  :
        - La couleur
        - Le titre
        - La description
        - L'url de l'image à insérer
        - L'url du lien sur doit être redirigé la personne lorsqu'elle clique sur le titre """

    def __init__(self, color, title, description, url):
        self.format = discord.Embed(color=color, title=title, description=description)
        self.format.set_thumbnail(url=url)
        self.format.set_footer(text="Extended Virtual Entity - Version 3.1")