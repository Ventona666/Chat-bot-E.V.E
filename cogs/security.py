# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Main file allowing automated moderation of a discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------


import os
import time
import discord
import asyncio
import psycopg2
from logs import logs
from guard import nuke_guard
from guard import raid_guard
from guard import spam_guard
from guard import selfbot_guard
from guard import profanity_guard
from datetime import datetime
from discord.utils import get
from discord.utils import find
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur
from googleapiclient import discovery
from better_profanity import profanity


class CounterMeasure:
    """ Classe définissant ce qui compose une contre-mesure, à savoir :
        - Son code
        - Sa description lors de l'activation
        - Sa description lors de la désactivation """

    def __init__(self, code, activation, deactivation):
        self.code = code
        self.activation = activation
        self.deactivation = deactivation


class Security(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed
        self.profanity = profanity
        self.profanity.load_censor_words_from_file("cogs/data/profanity.txt")
        self.cached_members = []
        self.countermeasures = [CounterMeasure(1, "Création d'un salon temporaire durant l'incident.", "Suppression du salon temporaire dans une minute"),
                                CounterMeasure(2, "Verrouillage des salons textuels.", "Déverrouillage des salons textuels."),
                                CounterMeasure(3, "Kick automatique des arrivants.", "Les nouveaux arrivants sont acceptés.")]


    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ Fonction qui se déclenche automatiquement à l'arrivée d'une personne. Permet de :
            - Souhaiter la bienvenue aux nouveaux membres, sauf si un raid est en cours
            - Kick automatiquement les nouveaux membres si un raid est en cours
            - Prévenir lors de l'ajout d'un bot """

        if str(member.guild.me.nick) == "E.V.E - Emergency Protocol":
            await kick(self, member, reason = "Mon protocole d'urgence a été activé suite à un incident sur le serveur. Vous ne pouvez pas rejoindre le serveur tant que mon protocole est actif. Si vous souhaiter le rejoindre, patientez un peu le temps que l'incident soit clôt.")
        else:
            if not member.bot:
                message = self.embed(self.couleur.blueColor, "E.V.E - Présentation", "Intelligence Artificielle", self.couleur.blueImageEve)
                message.format.add_field(name="Initialisation du module de bienvenue en cours...", value=f"Bienvenue {member.mention} sur le serveur ! Je m'appelle E.V.E, je suis un Chat bot doté d'intelligence artificielle, je suis là pour vous aidez et vous pouvez me faire aveuglément confiance, en toutes circonstances ! Equipée des dernières innovations technologiques, je suis polyvalente, mes systèmes sont régulièrement mis à jour. Je vous ai attribué le rôle de Membre sur le serveur. Si vous voulez voir l'ensemble des commandes que je peux effectuer, je vous invite à taper la commande !aide")
                await member.send(content=None, embed=message.format)
            else:
                await bot_detected(self, member)

            await new_user(self, member.id, member.guild.id, time.time())
            await auto_role(self, member)
            await raid_guard.raid_detection(self, member, time.time())


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ Fonction se déclenchant lors du départ d'un membre, permet d'effacer ses données dans la base de donnée """

        try:
            self.eve.cur.execute(f"DELETE FROM users WHERE user_id='{member.id}' AND guild_id='{member.guild.id}'")
            self.eve.conn.commit()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await nuke_guard.logs_channel_create(self, channel.guild)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await nuke_guard.logs_role_create(self, role.guild)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await nuke_guard.logs_role_delete(self, role.guild)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await nuke_guard.logs_channel_delete(self, channel.guild)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """ Fonction déclenchée automatiquement à chaque envoi d'un message dans un serveur """

        if ctx.channel.type == discord.ChannelType.text:
            if not ctx.guild.me == ctx.author:
                if ctx.type == discord.MessageType.default:
                    author_id = str(ctx.author.id)
                    guild_id = str(ctx.guild.id)

                    await lvl_system(self, author_id, guild_id, ctx)
                    await selfbot_guard.anti_selfbot(self, ctx.author, ctx.guild, ctx)
                    await spam_guard.anti_spam(self, author_id, guild_id, ctx)
                    await profanity_guard.content_analyse(self, ctx)

        elif ctx.channel.type == discord.ChannelType.private:
            if ctx.author.id != 769657665201897493:
                await selfbot_guard.verification(self, ctx)


    def convert(argument):
        sep = " "
        arg = argument.split()
        if arg[0].isdigit():
            return int(arg[0]), sep.join(arg[1:])
        return None, argument


    def cap(argument):
        return argument.capitalize()


    def bool_state(argument):
        arg = cap(argument)
        if arg == "On":
            return True
        elif arg == "Off":
            return False


    @commands.command()
    async def emergency(self, ctx, state):
        """ Permet d'activer ou de désactiver le protocole d'urgence de E.V.E """

        admin_access_level = await access_level(self, ctx, ctx.author)
        if admin_access_level > 1:
            member = get(ctx.guild.roles, name="Member")
            superviseur = get(ctx.guild.roles, name="Superviseur")
            master = get(ctx.guild.roles, name="Master")

            if state == "on":
                await emergency_protocol(self, f"Activation de mon Emergency Protocol par {ctx.author.mention}", f"L'Emergency Protocol est désormais actif. Tous les {member.mention} sont invités à ne pas céder à la panique et à informer les {superviseur.mention} et les {master.mention} de toute activité suspecte. Merci pour votre compréhension.", ctx.guild)
            elif state == "off":
                await disable_emergency_protocol(self, f"Désactivation de mon Emergency Protocol par {ctx.author.mention}", f"L'Emergency Protocol est désormais désactivé. Merci à tous les {member.mention} d'avoir respecté les consignes et nous pouvons féliciter les {superviseur.mention} et les {master.mention} pour la gestion de cette crise.", ctx.guild)
            else:
                message = self.embed(self.couleur.redColor, "E.V.E - Erreur", "Commande mal utilisée", self.couleur.redImageEve)
                message.format.add_field(name="Chargement de l'erreur", value="Vous pouvez activer le protocole d'urgence !emergency on et le désactiver en écrivant !emergency off")
                await ctx.author.send(content=None, embed=message.format)
        else:
            await access_denied(self, ctx)


    @commands.command(name="mod")
    async def moderation(self, ctx, sanction : cap, name : discord.Member, *, details : convert):
        """ Fonction permettant à un administrateur d'utiliser les fonctions :
            - Warn pour avertir un membre
            - Mute pour muter un membre
            - Unmute pour supprimer le mute appliqué à un membre
            - Kick pour exclure un membre
            - Ban pour bannir un membre """


        admin_access_level = await access_level(self, ctx, ctx.author)

        if sanction in ["Warn", "Mute", "Unmute", "Kick", "Ban"]:
            if sanction == "Warn" and admin_access_level > 1:
                await logs.member_log(self, name, sanction, details[1], ctx.author)
            elif sanction == "Mute" and admin_access_level > 1:
                return await mute(self, name, ctx.guild, reason[0]*60)
            elif sanction == "Unmute" and admin_access_level > 1:
                await unmute(self, name, ctx.guild)
            elif sanction == "Kick" and admin_access_level > 1:
                await kick(self, name)
            elif sanction == "Ban" and admin_access_level > 2:
                await ban(self, name)
            else:
                return await access_denied(self, ctx)

            await staff_logs(self, ctx, name, ctx.author.id, sanction, details[1], details[0])
            await member_log(self, ctx.author, sanction, details[1], ctx.author, details[0])

        else:
            error_message = self.embed(self.couleur.redColor, f"E.V.E - Erreur", "Voici le rapport détaillé de la situation.", self.couleur.redImageEve)
            error_message.format.add_field(name="Sanction non existente !", value=f"Désolé {ctx.author.mention} mais la sanction que vous avez spécifié, à savoir '{sanction}' n'est pas une sanction valide. Je vous informe que vous pouvez appliquer seulement un Warn, un Mute, un Unmute, un Kick ou encore un Ban.")
            await ctx.send(content=None, embed=error_message.format, delete_after=20)


    @moderation.error
    async def moderation_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            error_message = self.embed(self.couleur.redColor, "E.V.E - Erreur", "Voici le rapport détaillé de la situation.", self.couleur.redImageEve)
            error_message.format.add_field(name="Membre non trouvé !", value=f"Toutes mes excuses {ctx.author.mention} mais je rencontre des difficultés dans l'identification du membre que vous m'avez spécifié dans la commande de modération. Je suis donc dans l'incapacité d'appliquer une sanction. Veuillez vérifier que vous avez correctement orthographié le nom du membre visé.")
            await ctx.send(content=None, embed=error_message.format, delete_after=20)


async def mute(self, author, guild, duration):
    """ Fonction appliquant un mute temporairement à un membre d'un serveur """

    self.eve.cur.execute(f"INSERT INTO mutes (user_id, guild_id, mute) VALUES ('{author.id}', '{guild.id}', {time.time() + float(duration)})")
    self.eve.conn.commit()

    member = get(guild.roles, name="Member")
    mute = get(guild.roles, name="Mute")

    await author.remove_roles(member)
    await author.add_roles(mute)
    await asyncio.sleep(duration)
    await unmute(self, author, guild)


async def unmute(self, author, guild):
    """ Fonction levant un mute temporaire appliqué à un membre d'un serveur """

    self.eve.cur.execute(f"DELETE FROM mutes WHERE user_id = '{author.id}' AND guild_id = '{guild.id}'")
    self.eve.conn.commit()

    mute = get(guild.roles, name="Mute")
    member = get(guild.roles, name="Member")

    await author.remove_roles(mute)
    await author.add_roles(member)


async def kick(self, author, reason=None):
    """ Kick un membre """
    await author.kick(reason=reason)


async def ban(self, author, reason=None):
    """ Ban un membre """
    await author.ban(reason=reason)


async def access_level(self, ctx, admin):
    """ Fonction vérifiant les autorisations d'un membre et renvoyant :
        - Un niveau d'accès 1 si c'est un membre classique
        - Un niveau d'accès 2 si c'est un superviseur
        - Un niveau d'accès 3 si c'est un master ou une intelligence artificielle """

    superviseur = get(ctx.guild.roles, name="Superviseur")
    master = get(ctx.guild.roles, name="Master")
    intelligence_artificielle = get(ctx.guild.roles, name="Intelligence Artificielle")

    if intelligence_artificielle in admin.roles or master in admin.roles:
        return 3
    elif superviseur in admin.roles:
        return 2
    else:
        return 1


async def access_denied(self, ctx):
    """ Fonction informant un utilisateur qu'il n'a pas les droits requis pour exécuter certaines commandes """

    message = self.embed(self.couleur.redColor, "E.V.E - Accès Refusé", "Niveau d'accès insuffisant", self.couleur.redImageEve)
    message.format.add_field(name="Rapport détaillé", value=f"Cette commande nécessite un niveau d'accès plus élevé que celui que vous possédez. Je ne peux donc pas exécuter la commande souhaitée.")
    await ctx.author.send(content=None, embed=message.format)


async def auto_role(self, member):
    """ Fonction permettant d'attribuer le rôle de Membre aux nouveaux membres"""

    member_role = get(member.guild.roles, name="Member")
    await member.add_roles(member_role)


async def bot_detected(self, member):
    """ Fonction permettant d'avertir le propriétaire du serveur, tout les autres Masters et Superviseurs de l'ajout
        d'un autre bot """

    message = self.embed(self.couleur.redColor, "E.V.E - Sécurité du serveur potentiellement compromise !", "Un Chat bot a été ajouté au serveur", self.couleur.redImageEve)
    message.format.add_field(name="Voici le rapport détaillé", value=f"Mes systèmes détectent l'arrivée d'un nouveau Chat bot dans le serveur. Si vous approuvez cet ajout, alors la sécurité du serveur n'est pas compromise. Néanmoins si cet ajout n'est pas volontaire ou voulu, je vous mets en garde sur certaines I.A qui peuvent être destructrice pour le serveur. Si je détecte une autre activité suspecte je vous préviendrai.")

    text_channel = find(lambda x: x.name == 'rapport-eve', member.guild.text_channels)
    if text_channel:
        await text_channel.send(content=None, embed=message.format)
    await member.guild.owner.send(content=None, embed=message.format)


async def new_user(self, author_id, guild_id, joined_at):
    """ Fonction permettant d'ajouter un nouvel utilisateur à la base de donnée et de gérer le cache des nouveaux
        membres """

    if len(self.cached_members) > 100:
        del self.cached_members[0]

    self.cached_members.append((author_id, guild_id, joined_at))

    self.eve.cur.execute(f"INSERT INTO users (user_id, guild_id, level, experience, money, offense, necklace) VALUES ({author_id}, {guild_id}, 1, 0, 0, 0, FALSE)")
    self.eve.conn.commit()


async def restore_connection(self):
    """ Fonction permettant de rétablier la connexion à la base de donnée """

    self.eve.conn = psycopg2.connect(self.eve.DATABASE_URL, sslmode='require')
    self.eve.cur = self.eve.conn.cursor()


async def user_progress(self, author_id, guild_id):
    """ Fonction récursive permettant d'obtenir la progression du membre sur le serveur et de renvoyer :
        - Le niveau du membre
        - L'expérience du membre
        - L'argent du membre """

    try:
        self.eve.cur.execute(f"SELECT level, experience, money FROM users WHERE user_id = '{author_id}' AND guild_id = '{guild_id}'")
        level, experience, money = self.eve.cur.fetchone()
        return level, experience, money
    except psycopg2.InterfaceError:
        await restore_connection(self)
    except:
        await new_user(self, author_id, guild_id, time.time())

    return await user_progress(self, author_id, guild_id)


async def lvl_system(self, author_id, guild_id, ctx):
    """ Fonction permettant un système de niveau et d'économie pour les membres du serveur """

    level, experience, money = await user_progress(self, author_id, guild_id)
    next_level = int(experience**(1/4))

    self.eve.cur.execute(f"UPDATE users SET level = {next_level}, experience = experience+5, money = money+10 WHERE user_id = '{author_id}' AND guild_id = '{guild_id}'")
    self.eve.conn.commit()

    if level < next_level:
        congratulations = embed.Embed(couleur.Couleur().blueColor, "E.V.E - Niveau Supérieur !", "Ma base de donnée indique que vous avez passé un niveau", couleur.Couleur().blueImageEve)
        congratulations.format.add_field(name="Chargement du protocole...", value=f"Toutes mes félicitations {ctx.author.mention}, vous êtes désormais niveau {next_level} !")
        await ctx.channel.send(content = None, embed = congratulations.format , delete_after=15)


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


async def emergency_protocol(self, incident, details, guild):
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


async def disable_emergency_protocol(self, incident_end, details, guild):
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
    eve.add_cog(Security(eve))
