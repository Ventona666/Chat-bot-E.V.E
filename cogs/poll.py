# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Poll V2 for discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import discord
import matplotlib.pyplot as plt
from cogs.affichage import couleur
from cogs.affichage import embed
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed
        self.emoji_number = ("1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟")
        self.polls = list()
        self.polls_responds = dict()


    def parser(query, question = list(), proposal = list(), proposals = list(), i = 0, end = False):
        """ Fonction permettant de séparer la question des propositions """

        query_length = len(query)
        while i < query_length and not end:
            question.append(query[i])
            if query[i] == "?":
                question = "".join(question)
                end = True
            i += 1

        while i <= query_length:
            if i == query_length or query[i] == "/":
                proposal = "".join(proposal)
                proposals.append(proposal)
                proposal = list()
            else:
                proposal.append(query[i])
            i += 1

        return (question, proposals)


    @commands.command()
    async def poll(self, ctx, *, query : parser, i = 1, j = 0):
        """ Fonction affichant la question ainsi que les différentes réponses possible """

        message = self.embed(self.couleur.blueColor, "E.V.E - Sondage", f"Le membre {ctx.author.mention} a créé un sondage, vous tous invitez à y répondre", self.couleur.blueImageEve)
        message.format.add_field(name="Question", value=query[0])
        for proposal in query[1]:
            message.format.add_field(name=f"Proposition n°{i}", value=proposal, inline=False)
            i += 1
        message = await ctx.channel.send(content=None, embed=message.format)

        for loop in range(i-1):
            await message.add_reaction(self.emoji_number[j])
            j += 1

        self.polls.append((ctx.channel.id, message.id))
        self.polls_responds[ctx.channel.id] = [0,0,0,0]


    @commands.command()
    async def poll_graph(self, ctx, i = 0):
        """ Permet de tracer un graphique sur le sondage précédemment réalisé """

        barWidth = 0.8
        bars1, bars2, bars3, bars4 = self.polls_responds[ctx.channel.id]

        r1 = [1]
        r2 = [2]
        r3 = [3]
        r4 = [4]

        plt.clf()
        plt.bar(r1, bars1, width=barWidth, color='#1DA1F2', edgecolor='w')
        plt.bar(r2, bars2, width=barWidth, color='#5f72f6', edgecolor='w')
        plt.bar(r3, bars3, width=barWidth, color='#ae3afa', edgecolor='w')
        plt.bar(r4, bars4, width=barWidth, color='#F209FE', edgecolor='w')

        plt.xticks([1, 2, 3, 4], ["Réponse " + chr(i) for i in range(65, 69)])
        plt.savefig('cogs\data\graphSondage.png', facecolor='#2f3136', transparent=True)

        file = discord.File("cogs\data\graphSondage.png", filename="graphSondage.png")

        message = self.embed(self.couleur.blueColor, "E.V.E - Résultat du Sondage", f"Le sondage est désormais terminé. Voici un graphique de la répartition des votes. Merci à tous pour votre participation !", self.couleur.blueImageEve)
        message.format.set_image(url="attachment://graphSondage.png")
        await ctx.channel.send(file=file, content=None, embed=message.format)
        del self.polls_responds[ctx.channel.id]

        while i < len(self.polls):
            if self.polls[i][0] == ctx.channel.id:
                del self.polls[i]
            i += 1


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload, i = 0, verification = False):
        """ Fonction détectant les réactions à des messages """

        if payload.message_id in (poll[1] for poll in self.polls) and not payload.member.bot:
            message = await self.eve.get_channel(payload.channel_id).fetch_message(payload.message_id)
            for number in self.emoji_number:
                if payload.emoji.name == number:
                    self.polls_responds[payload.channel_id][i] += 1
                    verification = True
                i += 1

            if not verification:
                await message.remove_reaction(payload.emoji, payload.member)

            for reaction in message.reactions:
                if (payload.member in await reaction.users().flatten()) and (reaction.emoji != payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, payload.member)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload, i = 0):
        """ Fonction détectant la suppression de réaction """

        if payload.message_id in (poll[1] for poll in self.polls):
            message = await self.eve.get_channel(payload.channel_id).fetch_message(payload.message_id)
            for number in self.emoji_number:
                if payload.emoji.name == number:
                    self.polls_responds[payload.channel_id][i] -= 1
                i += 1


def setup(eve):
    eve.add_cog(Poll(eve))