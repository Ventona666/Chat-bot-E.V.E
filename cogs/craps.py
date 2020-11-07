# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Craps function design for discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import random
import discord
import asyncio
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur


class Craps(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed
        self.casino_token = ["⚪", "🔴", "🔵", "🟢", "⚫"]
        self.casino_bet_first_phase = ["🇦", "🇧"]
        self.casino_bet = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱"]
        self.craps_table = []
        self.craps_bet = dict()
        

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """ Fonction détectant les réactions à des messages """

        message = await self.eve.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.message_id in (table[1] for table in self.craps_table):
            if not payload.emoji.name in self.casino_token and not payload.emoji.name in self.casino_bet_first_phase :
                await message.remove_reaction(payload.emoji, payload.member)
            for reaction in message.reactions:
                if (payload.member in await reaction.users().flatten()) and (reaction.emoji != payload.emoji.name):
                    if not payload.member.bot and (str(reaction.emoji) in self.casino_token) and (payload.emoji.name in self.casino_token):
                        await message.remove_reaction(reaction.emoji, payload.member)
                    if not payload.member.bot and (str(reaction.emoji) in self.casino_bet_first_phase) and (payload.emoji.name in self.casino_bet_first_phase):
                        await message.remove_reaction(reaction.emoji, payload.member)

            for game in self.craps_bet.keys():
                if game == str(payload.message_id):
                    for user in self.craps_bet[game].keys():
                        if user == str(payload.member.id):
                            self.craps_bet[game][user].append(payload.emoji.name)
            bet_dict = dict()

            for reaction in message.reactions:
                x = []
                for user in await reaction.users().flatten():
                    x.append(user.id)

                bet_dict[str(reaction.emoji)] = x
            self.craps_bet[payload.message_id] = bet_dict

    @commands.command()
    async def craps_rules(self, ctx):
        """ Fonction permettant de donner les règles du craps """

        rules = embed.Embed(self.couleur.blueColor, "E.V.E - Casino OMEGA", "Les règles du craps", self.couleur.blueImageEve)
        rules.format.add_field(name="Première phase du jeu", value="Un lanceur sera désigné, ce sera la personne qui aura invoquée la commande pour lancer la partie de craps. Ensuite tous les joueurs misent une somme sur la 'Pass Line' ou sur 'Don't Pass'. Autrement dit, soit ils misent sur le fait que le lanceur va passer ou non. Le lanceur ne passe pas si la somme des deux dés est égale à 2, 3 ou 12 qui sont des craps, dans ce cas la partie est déjà terminé.")
        rules.format.add_field(name="")

    @commands.command()
    async def craps(self, ctx):
        """ Fonction permettant de jouer au craps """

        welcome = embed.Embed(self.couleur.blueColor, "E.V.E - Casino OMEGA", "Le craps", self.couleur.blueImageEve)
        welcome.format.add_field(name="Bienvenue autour de la table de craps", value="Le craps est un jeu dont le déroulement est très précis, mais aussi très intéressant. Si vous ne connaissez pas les règles du jeu, je vous invite à taper la commande !craps_rules")

        await ctx.channel.send(content=None, embed=welcome.format)

        await first_phase(self,ctx)
        await second_phase(self, ctx)

async def roll_dice():
    """ Fonction permettant de simuler le lancé de deux dés """

    return random.randint(1,6), random.randint(1,6)


async def shooter_victory(self, message_id):
    """ Fonction permettant de déclarer vainqueur le lanceur """

    bet = self.craps_bet[message_id]
    stake = []

    for key, value in bet.items():
        if key == "🇦":
            winners = value
        elif key == "🇧":
            loosers = value
        else:
            stake.append(bet[key])

    print(winners, loosers, stake)

async def shooter_defeat(self, message_id):
    """ Fonction permettant de déclarer la défaite du lanceur """

async def point(self, number, message_id):
    """ Fonction permettant de déterminer le point """

async def first_phase_case(self, dice_1, dice_2, message_id):
    """ Fonction permettant de savoir quelles mises sont gagnantes """

    result = dice_1 + dice_2

    if result in [7,11]:
        return await shooter_victory(self, message_id)
    elif result in [2,3,12]:
        return await shooter_defeat()
    return await create_point()


async def first_phase(self, ctx):
    """ Fonction permettant d'effectuer la première phase de jeu au craps """

    message = embed.Embed(self.couleur.blueColor, "E.V.E - Casino OMEGA", "Craps - Première Phase", self.couleur.blueImageEve)
    message.format.add_field(name="Chargement de la phase n°1", value=f"Le lanceur est {ctx.author.mention}. Maintenant tous les joueurs sont invités à placer leur mise sur la 'Pass Line' ou 'Don't Pass'. Vous avez 30 secondes pour miser.", inline=False)
    message.format.add_field(name="Les paris possibles", value = ":regional_indicator_a: = Pass Line\n"
                                                                 ":regional_indicator_b: = Don't Pass Bar\n")

    message.format.add_field(name="Les mises possibles", value = "⚪ = 10 crédits\n"
                                                                 "🔴 = 25 crédits\n"
                                                                 "🔵 = 50 crédits\n"
                                                                 "🟢 = 100 crédits\n"
                                                                 "⚫ = 500 crédits\n")

    message = await ctx.channel.send(content=None, embed=message.format)

    for bet in self.casino_bet_first_phase:
        await message.add_reaction(bet)

    for token in self.casino_token:
        await message.add_reaction(token)

    self.craps_table.append((ctx.channel.id, message.id))
    await asyncio.sleep(30)

    dice_1, dice_2 = await roll_dice()
    await first_phase_case(self, dice_1, dice_2, message.id)

    message = embed.Embed(self.couleur.blueColor, "E.V.E - Casino OMEGA", "Craps - Première Phase", self.couleur.blueImageEve)
    message.format.add_field(name="Phase n°1", value=f"Les paris sont désormais clôts. {ctx.author.mention} va lancer les deux dés.")
    message.format.add_field(name="Premier :game_die:", value=f"C'est un {dice_1} !")
    message.format.add_field(name="Deuxième :game_die:", value=f"C'est un {dice_2} !")


async def second_phase(self, ctx):
    """ Fonction permettant le déroulement de la deuxième phase de jeu du craps """

    message = embed.Embed(self.couleur.blueColor, "E.V.E - Casino OMEGA", "Craps - Deuxième Phase", self.couleur.blueImageEve)
    message.format.add_field(name="Chargement de la phase n°2", value=f"Voici la deuxième phase du jeu. Le lanceur, {ctx.author.mention} à obtenu {point}, cela détermine donc le point. Tous les joueurs sont invités à placer ou non une mise parmis les suivantes. Vous avez 30 secondes pour miser.", inline= False)
    message.format.add_field(name="Les paris possibles", value=":regional_indicator_a: = Come\n"
                                                               ":regional_indicator_b: = Don't Come\n"
                                                               ":regional_indicator_c: = Big 6\n"
                                                               ":regional_indicator_d: = Big 8\n"
                                                               ":regional_indicator_e: = Any 7\n"
                                                               ":regional_indicator_f: = Any 11\n"
                                                               ":regional_indicator_g: = Field bet\n"
                                                               ":regional_indicator_h: = Any Craps\n"
                                                               ":regional_indicator_i: = Horn Bet sur le 3 ou 11\n"
                                                               ":regional_indicator_j: = Horn Bet sur le 2 ou 12\n"
                                                               ":regional_indicator_k: = Hardway sur le 4 ou 10\n"
                                                               ":regional_indicator_l: = Hardway sur le 6 ou 8\n")

    message.format.add_field(name="Les mises possibles", value="⚪ = 10 crédits\n"
                                                               "🔴 = 25 crédits\n"
                                                               "🔵 = 50 crédits\n"
                                                               "🟢 = 100 crédits\n"
                                                               "⚫ = 500 crédits\n")

    message = await ctx.channel.send(content=None, embed=message.format)

    for bet in self.casino_bet:
        await message.add_reaction(bet)

    for token in self.casino_token:
        await message.add_reaction(token)

def setup(eve):
    eve.add_cog(Craps(eve))
