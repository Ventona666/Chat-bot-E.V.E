# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Leaderboard and rank for discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------


import os
import discord
from discord.utils import get
from discord.utils import find
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur

class Acces(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def rank(self, ctx):
        """ Fonction permettant d'accéder au rank d'un membre du serveur """

        self.eve.cur.execute(f"SELECT user_id, guild_id, level, experience, money, offense FROM users WHERE guild_id = '{ctx.guild.id}'")
        guild = self.eve.cur.fetchall()
        guild_sort = tri_rapide(guild)
        i = len(guild)

        for member in guild_sort:
            if member[0] == str(ctx.author.id):
                user = member
                break
            i -= 1

        info = self.embed(self.couleur.blueColor, "E.V.E - Rank", f"Voici toutes les informations relatives à votre compte, {ctx.author.mention}.", ctx.author.avatar_url)
        info.format.add_field(name="Rang", value=f"Vous êtes au rang #{i} dans le serveur.", inline=False)
        info.format.add_field(name="Niveau", value=f"Vous êtes niveau {user[2]} avec {user[3]} points d'expérience.")
        info.format.add_field(name="Argent", value=f"Vous avez accumulé la somme de {user[4]} crédits.")
        info.format.add_field(name="Infractions", value=f"Vous avez commis {user[5]} infraction(s) sur le serveur.")
        await ctx.channel.send(content=None, embed=info.format)

    @commands.command()
    async def leaderboard(self, ctx):
        """ Fonction affichant le rank des membres d'un serveur """

        self.eve.cur.execute(f"SELECT user_id, guild_id, level, experience FROM users WHERE guild_id = '{ctx.guild.id}'")
        guild = self.eve.cur.fetchall()
        guild_sort = tri_rapide(guild)

        i = len(guild_sort)-1
        j = 1
        info = self.embed(self.couleur.blueColor, "E.V.E - Leaderboard", f"Voici le classement des membres du serveur.", self.couleur.blueImageEve)
        while i >= 0 and j <= 10:
            try:
                user = await ctx.guild.fetch_member(int(guild_sort[i][0]))
                info.format.add_field(name=f":beginner: Rang n°{j} - {user}", value=f"*Niveau {guild_sort[i][2]} | Point d'expérience : {guild_sort[i][3]}*", inline=False)
                j += 1
            except:
                pass
            i -= 1
        await ctx.channel.send(content=None, embed=info.format)

def tri_rapide(tableau):
    if not tableau:
        return []
    else:
        pivot = tableau[-1][3]
        plus_petit = [x for x in tableau     if x[3] <  pivot]
        plus_grand = [x for x in tableau[:-1] if x[3] >= pivot]
        return tri_rapide(plus_petit) + [tableau[-1]] + tri_rapide(plus_grand)

def setup(eve):
    eve.add_cog(Acces(eve))
