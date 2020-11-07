# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Anti-Selfbot for discord server
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import random
import discord
from logs import logs
from cogs import security
from datetime import datetime
from discord.utils import get
from discord.utils import find
from captcha.image import ImageCaptcha

ascii_carac = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
awaiting_verification = {}


async def verification(self, message, i = 1):
    """ Fonction vérifiant si le contenu saisi par l'utilisateur est correcte vis-à-vis du captcha """

    for user in awaiting_verification.keys():
        if user == message.author:
            if message.content.startswith(awaiting_verification[user][0]):
                logs = self.embed(self.couleur.blueColor, f"E.V.E - Vérification réussi", f"Vous avez bien prouvé que vous n'êtes pas un selfbot {message.author.mention}. Je vous prie d'accepter toutes mes excuses pour ce malentendu.", self.couleur.redImageEve)
                await message.author.send(content=None, embed=logs.format)
                while i < len(awaiting_verification[user]):
                    await security.unmute(self, user, awaiting_verification[user][i])
                    i += 1
                del awaiting_verification[user]
            else:
                await anti_selfbot(self, message.author, awaiting_verification[user][1], message)
            break


async def captcha_generator(self, author, guild, ctx):
    """ Fonction générant un captcha et l'envoyant sur le canal dédié """

    code = random.sample(ascii_carac, k=6)
    code = "".join(code)
    image = ImageCaptcha()
    data = image.generate(code)
    image.write(code, "cogs\data\captcha.png")
    file = discord.File("cogs\data\captcha.png", filename="captcha.png")

    notification = self.embed(self.couleur.redColor, f"E.V.E - Vérification", f"Excusez-moi {author.mention}, mes systèmes détectent une activité suspecte de votre part, je vous soupçonne d'être un selfbot, je vous ai mute pour une durée de 6h, néanmoins si vous résolvez le captcha suivant, j'enlèverai la sanction.", self.couleur.redImageEve)
    notification.format.set_image(url="attachment://captcha.png")
    await author.send(file=file, content=None, embed=notification.format)

    if not author in awaiting_verification:
        awaiting_verification[author] = [code, guild]
    else:
        awaiting_verification[author][0] = code
    if not guild in awaiting_verification[author]:
        awaiting_verification[author].append(guild)


async def anti_selfbot(self, author, guild, ctx):
    """ Fonction permettant de vérifier que les messages envoyés sont :
        - Bien différent les uns des autres
        - La durée entre chaque message est différente
        - L'utilisateur reçoit un nombre cohérent de réponse """


    def _check_last_message(m):
        return (datetime.utcnow() - m.created_at).seconds < 300

    def _check_same_author(m):
        return m.author == author

    def _check_same_channel(m):
        return m.channel == ctx.channel

    def _check_same_content(m):
        return m.content == ctx.content

    last_message = list(filter(lambda m: _check_last_message(m), self.eve.cached_messages))
    same_author = list(filter(lambda m: _check_same_author(m), last_message))
    same_channel = list(filter(lambda m: _check_same_channel(m), same_author))
    same_content = list(filter(lambda m: _check_same_content(m), same_channel))

    intervals = list()
    i = len(same_channel)-1
    j = 0

    while i > 0:
        intervals.append((same_channel[i-1].created_at-same_channel[i].created_at).seconds)
        if i < len(same_channel) - 2:
            if intervals[j] == intervals[j+1]:
                j += 1
        i -= 1

    if len(same_channel) // 3 > len(list(filter(lambda m: _check_same_channel(m), last_message))) - len(same_channel) and len(same_channel) > 15 or len(same_content) > 10 or j > 2:
        await captcha_generator(self, author, guild, ctx)
        if not get(ctx.guild.roles, name="Mute") in ctx.author.roles:
            await security.mute(self, ctx.author, ctx.guild, 21600)