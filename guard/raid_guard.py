# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Anti raid for discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import discord
import asyncio
from cogs import security
from discord.utils import get
from discord.utils import find
from datetime import datetime
from cogs.affichage import embed
from cogs.affichage import couleur

async def channel_manager(self, guild, authorization):
    """ Fonction permettant de verrouiller les salons textuels """

    for channel in guild.channels:
        if channel.type == discord.ChannelType.text:
            await channel.set_permissions(get(guild.roles, name="Member"), send_messages = authorization)


async def channel_creater(self, guild):
    """ Permet la création d'un salon textuel temporaire pour les membres du serveur durant un incident """

    await guild.create_text_channel(name='salon-temporaire', topic="Salon temporaire durant l'incident")


async def channel_suppressor(self, guild):
    """ Permet la suppression du salon textuel temporaire """

    channel = find(lambda x: x.name == 'salon-temporaire', guild.text_channels)
    if channel:
        decision = embed.Embed(couleur.Couleur().blueColor, "E.V.E - Information", "Suppresion du salon", couleur.Couleur().blueImageEve)
        decision.format.add_field(name="Rapport de le situation", value="Suite à la désactivation de mon protocole d'urgence, ce salon textuel va être supprimé dans 1 minute, merci de votre compréhension.")
        await channel.send(content=None, embed=decision.format)
        await asyncio.sleep(60)
        await channel.delete()


async def arrivals(self, guild, beginning):
    """ Fonction détectant un flux important de nouveau membre sur le serveur """

    i = len(self.cached_members)-1
    users = []
    recent_join = True

    while i >= 0 and recent_join:
        if self.cached_members[i][1] == guild.id:
            if self.cached_members[i][2] > beginning - 10.0:
                users.append(self.cached_members[i][0])
            else:
                recent_join = False
            i -= 1

    if len(users) > 5:
        await raid(self, guild, users)


async def raid(self, guild, users):
    """ Fonction permettant l'expulsion des derniers membres arrivés et mise en place du protocole d'urgence """

    for user in users:
        await security.kick(self, user, reason= "Mon protocole d'urgence a été activé suite à un incident sur le serveur. Vous ne pouvez pas rejoindre le serveur tant que mon protocole est actif. Si vous souhaiter le rejoindre, patientez un peu le temps que l'incident soit clôt.")

    membre = get(guild.roles, name="Member")
    superviseur = get(guild.roles, name="Superviseur")
    master = get(guild.roles, name="Master")

    await security.emergency_protocol(self, "Raid détecté", f"Attention ! Mes systèmes détectent un flux important de nouveaux membres sur le serveur. J'enclenche mon Emergency Protocol. Tous les {membre.mention} sont invités à ne pas céder à la panique et à informer les {superviseur.mention} et les {master.mention} de toute activité suspecte. Je vous informerai quand l'incident sera clôt. Merci pour votre compréhension.", guild)
    await raid_end_detection(self, member, beginning)


async def raid_end_detection(self, member, beginning, raid=True):
    """ Fonction détectant si le flux de nouveaux membre sur le serveur est normal """

    membre = get(ctx.guild.roles, name="Member")
    superviseur = get(ctx.guild.roles, name="Superviseur")
    master = get(ctx.guild.roles, name="Master")

    while raid:
        if beginning + 300.0 < time.time():
            attacker_number = await raid(self, member, beginning)
            if attacker_number > 5:
                await asyncio.sleep(300)
            else:
                raid = False
                await security.disable_emergency_protocol(self, incident_end="Fin du raid", details=f"Mes systèmes ne détectent plus de flux importants de personne sur le serveur, ceci indique donc la fin du raid. Merci à tous les {membre.mention} d'avoir respecté les consignes et nous pouvons féliciter les {superviseur.mention} et les {master.mention} pour la gestion de cette crise.", guild_id = member.guild.id)
        else:
            await asyncio.sleep(300)
