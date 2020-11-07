# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Emergency Protocol of E.V.E
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import time
import discord
import asyncio
from logs import logs
from guard import raid_guard
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur

class CounterMeasure:
    """ Classe définissant ce qui compose une contre-mesure, à savoir :
        - Son code
        - Sa description lors de l'activation
        - Sa description lors de la désactivation """

    def __init__(self, code, activation, deactivation):
        self.code = code
        self.activation = activation
        self.deactivation = activation

class Emergency(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed
        self.countermeasures = [CounterMeasure(1, "Création d'un salon temporaire durant l'incident.", "Suppression du salon temporaire dans une minute"),
                                CounterMeasure(2, "Verrouillage des salons textuels.", "Déverrouillage des salons textuels."),
                                CounterMeasure(3, "Kick automatique des arrivants.", "Les nouveaux arrivants sont acceptés.")]


async def eve_mode(self, guild, emergency):
    # Fonction changeant la couleur du pseudo de E.V.E et indique si le protocole d'urgence est activé.

    if emergency and str(guild.me.nick) != "E.V.E - Emergency Protocol":
        artificial_intelligence = get(guild.roles, name="Intelligence Artificielle")
        await artificial_intelligence.edit(colour=discord.Colour(0xff0000))
        await guild.me.edit(nick="E.V.E - Emergency Protocol")
        return True

    elif not emergency and str(guild.me.nick) == "E.V.E - Emergency Protocol":
        artificial_intelligence = get(guild.roles, name="Intelligence Artificielle")
        await artificial_intelligence.edit(colour=discord.Colour(0x00ffe5))
        await guild.me.edit(nick="E.V.E")
        return True

    else:
        return False


async def emergency_protocol(self, guild, incident, details):
    """ Fonction représentant le protocole d'urgence de E.V.E, le protocole peut :
        - Verrouiller les salons textuels
        - Expulser toute personne tentant de rejoindre le serveur
        - Création d'un salon textuel temporaire pour les membres du serveur
        - Envoi une notification à tous les membres du serveur sur l'incident en cours """

    if await eve_mode(self, guild, True):
        channel = find(lambda x: x.name == 'annonce', guild.text_channels)
        if channel:
            alert = embed.Embed(couleur.Couleur().redColor, "E.V.E - Emergency Protocol Activated", incident, guild.me.avatar_url)
            alert.format.add_field(name="Mode Anti-Raid activé. Chargement des contre-mesures", value = details, inline=False)
            for counter in self.countermeasures:
                alert.format.add_field(name=f"Contre-mesure n°{counter.code}", value=counter.activation)
            alert.format.add_field(name="Début de l'incident", value=f"{time.strftime('%c', time.localtime(time.time()))}")
            await channel.send(content=None, embed=alert.format)

        await raid_guard.channel_manager(self, guild, False)
        await raid_guard.channel_creater(self, guild)


async def disable_emergency_protocol(self, guild, incident_end, details):
    """ Fonction permettant la désactivation du protocole d'urgence de E.V.E """

    if await eve_mode(self, guild, False):
        await raid_guard.channel_manager(self, guild, True)

        channel = find(lambda x: x.name == 'annonce', guild.text_channels)
        if channel:
            notification = embed.Embed(couleur.Couleur().blueColor, "E.V.E - Emergency Protocol Disabled", incident_end, couleur.Couleur().blueImageEve)
            notification.format.add_field(name="Mode Anti-Raid désactivé. Chargement du rapport ...", value=details, inline=False)
            for counter in self.countermeasures:
                notification.format.add_field(name=f"Désactivation de la contre-mesure n°{counter.code}", value=counter.deactivation)
            notification.format.add_field(name="Fin de l'incident", value=f"{time.strftime('%c', time.localtime(time.time()))}")
            await channel.send(content=None, embed=notification.format)

        await raid_guard.channel_suppressor(self, guild)

def setup(eve):
    eve.add_cog(Emergency(eve))