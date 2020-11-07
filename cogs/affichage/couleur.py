# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Definition of color and avatar url of embed.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

class Couleur():
    """ Classe définissant certains paramètres utilisés par les embeds, à savoir :
        - L'adresse url du portrait de Eve, un en bleu et l'autre en rouge
        - Le code couleur utilisé pour définir le bleu et le rouge """

    def __init__(self):
        self.blueImageEve = 'https://cdn.discordapp.com/attachments/712966107916664852/766677614692663336/fsdf.jpg'
        self.blueColor = 0x1DA1F2
        self.redImageEve = 'https://cdn.discordapp.com/attachments/712966107916664852/766677614692663336/fsdf.jpg'
        self.redColor = 0xF209FE
