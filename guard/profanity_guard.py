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
from cogs import security
from logs import logs
from datetime import datetime
from cogs.affichage import embed
from cogs.affichage import couleur
from googleapiclient import discovery
from better_profanity import profanity


async def content_analyse(self, ctx):
    """ Analyse appronfondie des messages, à savoir:
        - Grâce à de l'intelligence artificielle, détermine la probabilité que le message soit haineux
        - Reconnaissance de toute insulte ou mot grossier, même modifié (ex: un @ à la place d'un a) """

    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey='AIzaSyC_JLz-oRhmLJhR-bQG1zFLfEyB-yA3zCY')
    analyze_request = {'comment': {'text': ctx.content}, 'requestedAttributes': {'TOXICITY': {}}}

    try:
        response = service.comments().analyze(body=analyze_request).execute()
        probability = response['attributeScores']['TOXICITY']['summaryScore']['value']
    except:
        probability = 0

    if probability > 0.60:
        await ctx.delete() # Suppresion du message
        await logs.staff_logs(self, ctx.guild, ctx.author, ctx.guild.me, 'Warn', f"Mon algorithme indique une probabilité de {probability * 100} % "
                                                                          "que le contenu du message posté par l'utilisateur contient "
                                                                          "des propos haineux. J'ai donc averti l'auteur de son "
                                                                          "mauvais comportement.")

        await logs.member_log(self, ctx.author, "Warn", f"Mes systèmes indique une probabilité de {probability * 100} % "
                                                   f"que le contenu de votre message soit haineux. J'ai donc signalé "
                                                   f"votre comportement aux Superviseurs et aux Masteurs du serveur. "
                                                   f"Je vous invite à adopter un langage plus approprié. Dans le cas "
                                                   f"contraire je serai dans l'obligation d'appliquer des sanctions.")

    elif self.profanity.contains_profanity(ctx.content):
        await ctx.delete()  # Suppresion du message
        await logs.staff_logs(self, ctx.guild, ctx.author, ctx.guild.me, 'Warn', f"Mon algorithme indique une probabilité de {probability * 100} % "
                                                                          "que le contenu du message posté par l'utilisateur contient "
                                                                          "des propos haineux. Cette probabilité est trop faible pour que je "
                                                                          "sanctionne l'auteur. Néanmoins, j'ai détecté une insulte ou un "
                                                                          "mot grossier. J'ai donc supprimé son message et l'ai averti sur "
                                                                          "son mauvais comportement.")

        await logs.member_log(self, ctx.author, "Warn", f"Mon algorithme indique la présence d'insultes ou de mots "
                                                   f"grossiers dans votre dernier message. J'ai donc signalé "
                                                   f"votre comportement aux Superviseurs et aux Masteurs du serveur. "
                                                   f"Je vous invite à adopter un langage plus approprié. Dans le cas "
                                                   f"contraire je serai dans l'obligation d'appliquer des sanctions.")