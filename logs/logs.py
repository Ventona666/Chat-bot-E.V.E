# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Logs for staff and member
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import time
import discord
import asyncio
from discord.utils import find
from datetime import datetime
from cogs.affichage import embed
from cogs.affichage import couleur


async def staff_logs(self, guild, target_member, admin, sanction, reason, duration=None):
    """ Fonction informant les membres du staff qu'un avertissement ou une sanction a été appliqué à un membre. """

    eve_report = find(lambda x: x.name == 'rapport-eve', guild.text_channels)

    logs = self.embed(self.couleur.redColor, f"E.V.E - {sanction}", "Voici le rapport détaillé de la situation.", self.couleur.redImageEve)
    logs.format.add_field(name="Membre visé", value=f":arrow_right: {target_member.mention} :arrow_left:")
    logs.format.add_field(name="Administrateur", value=f":arrow_right: {admin.mention} :arrow_left:")
    logs.format.add_field(name="Voici la raison", value=reason, inline=False)
    logs.format.add_field(name="Date et heure du rapport", value=f"{time.strftime('%c', time.localtime(time.time()))}")

    if duration:
        logs.format.add_field(name="Durée de la sanction", value=f"{duration} minute(s)")
    if eve_report:
        await eve_report.send(content=None, embed=logs.format)


async def member_log(self, author, sanction, reason, admin = None, duration = None):
    """ Fonction informant un membre qu'il a reçu un avertissement ou une sanction """

    if not author.bot:
        info = self.embed(self.couleur.redColor, f"E.V.E - {sanction}", "Voici le rapport détaillé de la situation.", self.couleur.redImageEve)
        if admin != None:
            info.format.add_field(name="Administrateur", value=f":arrow_right: {admin.mention} :arrow_left:", inline=False)
            info.format.add_field(name="Voici le rapport de l'administrateur", value=reason)
        else:
            info.format.add_field(name="Chargement du protocole", value=f"Attention {author.mention}, j'ai pris une décision à votre encontre suite à un incident.", inline=False)
            info.format.add_field(name="Voici mon rapport", value=reason)

        info.format.add_field(name="Date et heure du rapport", value=f"{time.strftime('%c', time.localtime(time.time()))}", inline=False)

        if duration:
            info.format.add_field(name="Durée de la sanction", value=f"{duration} minute(s)", inline=False)

        await author.send(content=None, embed=info.format)