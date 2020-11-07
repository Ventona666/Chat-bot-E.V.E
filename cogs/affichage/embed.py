# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Default embed for discord bot.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import discord
from discord.utils import get
from discord.ext import commands


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
