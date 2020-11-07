# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Logs analyzer and nuke protection from bots and administrators.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------


import discord
import asyncio
from logs import logs as lg
from datetime import datetime
from cogs.affichage import embed
from cogs.affichage import couleur

limits = {discord.AuditLogAction.channel_create : {"per_minute" : 5, "per_hour" : 12},
          discord.AuditLogAction.channel_delete : {"per_minute" : 5, "per_hour" : 12},
          discord.AuditLogAction.kick           : {"per_minute" : 7, "per_hour" : 14},
          discord.AuditLogAction.ban            : {"per_minute" : 7, "per_hour" : 14},
          discord.AuditLogAction.role_create    : {"per_minute" : 6, "per_hour" : 12},
          discord.AuditLogAction.role_delete    : {"per_minute" : 6, "per_hour" : 12}}

async def logs_channel_create(self, guild):
    return await logs_sorter(self, guild, discord.AuditLogAction.channel_create)

async def logs_channel_delete(self, guild):
    return await logs_sorter(self, guild, discord.AuditLogAction.channel_delete)

async def logs_member_remove(self, guild):
    return await logs_sorter(self, guild, discord.AuditLogAction.channel_create)

async def logs_role_create(self, guild):
    return await logs_sorter(self, guild, discord.AuditLogAction.role_create)

async def logs_role_delete(self, guild):
    return await logs_sorter(self, guild, discord.AuditLogAction.role_delete)

async def logs_sorter(self, guild, action):
    """ Vérifie que l'auteur du dernier log du serveur n'est pas en infraction """

    async for entry in guild.audit_logs(limit=1):
        admin = entry.user

    logs = guild.audit_logs(limit=100, action=action, user=admin)

    last_minute = list()
    last_hour = list()

    async for entry in logs:
        if (datetime.utcnow() - entry.created_at).seconds < 60:
            last_minute.append(entry)
            last_hour.append(entry)
        elif (datetime.utcnow() - entry.created_at).seconds < 3600:
            last_hour.append(entry)

    if not admin.id == 672521812315471883:
        if limits[action]["per_minute"] <= len(last_minute):
            return await admin_suspension(self, guild, admin, last_minute, action)
        elif limits[action]["per_hour"] <= len(last_hour):
            return await admin_suspension(self, guild, admin, last_hour, action)
        return None

async def admin_suspension(self, guild, admin, logs, action):
    """ Relève de ses fonctions un administrateur du serveur suite à incident """
    
    for role in admin.roles:
        if not role.name == '@everyone':
            await admin.remove_roles(role)

    sentences = {discord.AuditLogAction.channel_create : "Création du salon ",
                 discord.AuditLogAction.channel_delete : "Suppression du salon ",
                 discord.AuditLogAction.kick : "Kick du membre ",
                 discord.AuditLogAction.ban : "Ban du membre ",
                 discord.AuditLogAction.role_create : "Création du rôle ",
                 discord.AuditLogAction.role_delete : "Suppression du rôle "}

    reason = str()
    if action == discord.AuditLogAction.channel_create or action == discord.AuditLogAction.role_create:
        for l in logs:
            reason += sentences[action] + "`" + str(l.after.name) + "`" + " il y a " + str((datetime.utcnow() - l.created_at).seconds) + "secondes" + "\n"
    elif action == discord.AuditLogAction.channel_delete or action == discord.AuditLogAction.role_delete:
        for l in logs:
            reason += sentences[action] + "`" + str(l.before.name) + "`" + " il y a " + str((datetime.utcnow() - l.created_at).seconds) + "secondes" + "\n"
    else:
        for l in logs:
            reason += sentences[action] + "`" + str(l.target) + "`" + " il y a " + str((datetime.utcnow() - l.created_at).seconds) + "secondes" + "\n"

    await lg.member_log(self, admin, "Suspension", f"Suite à une anomalie détectée dans les logs du serveur, je suis donc dans l'obligation de vous relever de vos fonctions pour assurer l'intégrité du serveur. Les membres du Staff ont été informés de l'incident et ils devront déterminer si la sanction que j'ai appliqué à votre encontre est légitime ou non.\n\nRaison :\n{reason}")
    await lg.staff_logs(self, guild, admin, guild.me, "Suspension", f"Suite à une anomalie détectée dans les logs du serveur, j'ai suspendu l'administrateur afin de préserver l'intégrité du serveur. Tout administrateur ayant un niveau d'accès 3 sont priés de bien vouloir décider si la sanction que j'ai appliqué est justifié ou non. Merci de votre compréhension.\n\nRaison :\n{reason}")
