# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Help function.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------


import discord
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur

class Aide(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def aide(self, ctx):
        message = self.embed(self.couleur.blueColor, "E.V.E - Aide", "Voici l'ensemble des fonctionnalités disponibles", self.couleur.blueImageEve)

        message.format.add_field(name="=== Les fonctions basiques ===", value="Voici un petit ensemble de fonction utilitaire proposé par mon algorithme.", inline=False)
        message.format.add_field(name="!stats (aucun paramètre)", value=":bar_chart: Obtenir les statistiques détaillées du serveur.", inline=False)
        message.format.add_field(name="!timer (durée en minute)", value=":stopwatch: Enclenche un minuteur pour une valeur donnée.", inline=False)
        message.format.add_field(name="!poll (question ? prop_1 / prop_2...)", value=":clipboard: Faire un sondage.", inline=False)
        message.format.add_field(name="!poll_graph", value="Met fin au sondage précédemment effectué, affiche un graphique sur la répartition des votes", inline=False)
        message.format.add_field(name="!rank (aucun paramètre)", value=":blue_book: Affiche les informations liées à votre compte stockées sur ma base de donnée.", inline=False)
        message.format.add_field(name="!leaderboard (aucun paramètre)", value=":trophy: Affiche le classement des membes du serveur.", inline=False)
        message.format.add_field(name="!hunger_games (aucun paramètre)", value=":bow_and_arrow: Lance les Hungers Games !", inline=False)
        message.format.add_field(name="!support (aucun paramètre)", value=":incoming_envelope: Donne le lien du serveur support.", inline=False)

        message.format.add_field(name="=== Le store OMEGA ===", value="Bienvenue dans le store OMEGA, c'est le centre névralgique de l'économie du serveur, plusieurs items sont disponibles à la vente. ", inline=False)
        message.format.add_field(name="!store (aucun paramètre)", value=":department_store: Affiche les articles disponibles au store OMEGA.", inline=False)

        message.format.add_field(name="=== Le casino OMEGA ===", value="Bienvenue dans mon casino flambant neuf et virtuel ! Vous y trouverez une multitude de jeu de casino pour jouer seul ou à plusieurs.", inline=False)
        message.format.add_field(name="!slot (mise entre 50 et 500)", value=":slot_machine: Jouer aux machines à sous.", inline=False)
        message.format.add_field(name="!roulette (numéro, mise entre 50 et 500)", value=":radio_button: Jeu de la roulette.", inline=False)
        message.format.add_field(name="!craps", value=":name_badge: (En cours de développement) Jeu du craps, peut se jouer seul ou à plusieurs.", inline=False)

        message.format.add_field(name="=== Les fonction pour la modération ===", value="Mes systèmes ont été conçus pour analyser toutes les activités du serveur. Je suis doté d'un premier système utilisant de l'intelligence artificielle pour me permettre de détecter tout langage inapproprié, d'un deuxième pour les spams et d'un troisième pour les raids. Dans chacune de ces trois situations, des contre-mesures sont prévues et je les appliquerai automatiquement. Vous pouvez néanmoins utiliser les commandes suivantes si vous êtes un Superviseur ou un Master du serveur.")
        message.format.add_field(name="!emergency (on/off)", value=":beginner: Active ou de désactive mon protocole d'urgence. Très efficace pour contrer un raid.", inline=False)
        message.format.add_field(name="!mod warn (membre, raison)", value=":anger: Averti un membre sur son mauvais comportement.", inline=False)
        message.format.add_field(name="!mod mute (membre, durée, raison)", value=":face_with_symbols_over_mouth: Mute temporaire d'un membre.", inline=False)
        message.format.add_field(name="!mod unmute (membre, raison)", value=":innocent: Enlève un mute appliqué à un membre.", inline=False)
        message.format.add_field(name="!mod kick (membre, raison)", value=":dash: Kick d'un membre", inline=False)
        message.format.add_field(name="!mod ban (membre, raison)", value=":no_entry_sign: Banissement d'un membre", inline=False)
        message.format.add_field(name="!clear (nombre de message)", value=":wastebasket: Efface un ou plusieurs messages.", inline=False)

        await ctx.author.send(content=None, embed=message.format)

def setup(eve):
    eve.add_cog(Aide(eve))
