# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Hunger Games for discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import random
import discord
import asyncio
from cogs.affichage import embed
from cogs.affichage import couleur
from discord.ext import commands


class Arena:
    """ Classe définissant les caractéristiques d'une arène des Hungers Games, à savoir :
        - Le biome
        - Les armes
        - Les animaux
        - Les pièges """

    def __init__(self, biome, weapons, animals, traps):
        self.biome = biome
        self.weapons = weapons
        self.animals = animals
        self.traps = traps


class HungerGames(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed
        self.districts = dict()
        self.arena = [Arena("Urbaine", ["a été tué à coup de panneau de signalisation par", "s'est pris une plaque d'égout lancé par", "s'est fait décapiter avec un pavé par", "a succombé après les plusieurs coup violent de matraque"], ["se font poursuivre par une voiture autonome !", "se font poursuivre par des drones de combat !"], ["ont été les victimes d'un tremblement de terre !", "ont subit l'explosion d'une conduite de gaz !"]),
                      Arena("Tropicale", ["s'est pris une flèche de l'arc appartenant à", "a subit plusieurs coup du couteau de combat de", "s'est fait étripé par le trident de", "s'est pris un coup de machette par", "a été électrocuter par un fil de cuivre haute tension relié au bouclier de l'arène par"], ["se font attaquer par des singes mutants !", "deviennent complétement fou à cause de plusieurs geais moqueur !"], ["sont sous une pluie de sang !", "tente d'échapper à la fumée paralysante"]),
                      Arena("Neigeuse", ["se fait bombarder de boule de neige par", "a pris un bloc de glace en plein dans la tête à cause de", "a glissé et s'est fracturé la colonne vertébrale à cause du spray verglaçant utilisé par"], ["se font poursuivre par un ours polaire !", "sont en train de subir l'attaque de l'armée de pingouins robotique !"], ["se retrouve isolé sur un ice berg a cause de la fonte des glaces, ils vont devoir braver le froid s'ils veulent retourner sur le rivage !", "sont frigorifié a cause de la violente tempête de neige !"]),
                      Arena("Forestière", ["s'est pris une flèche de l'arc appartenant à", "a subit plusieurs coup du couteau de combat de", "s'est pris un coup de machette par", "a marché sur la mine placée par"], ["subissent les piqures des guêpes tueuses !", "se font poursuivre par des chiens mutants !"], ["courent pour éviter les boules de feu projetées sur eux !", "mangent des baies de sureau mortel !"]),
                      Arena("Martienne", ["a subit les tirs du pistolet laser de", "a asphyxié car sa combinaison était défaillante à cause de la bombe IEM lancé par", "a subit des coups surpuissant à cause de l'exosquelette trouvé par"], ["se battent contre les martiens !", "se font poursuivre par un vaisseau spatial"], ["subissent les radiations d'une éruption solaire !", "sont les victimes d'une tempête de sable !"])]

    @commands.command()
    async def hunger_games(self, ctx):
        """ Fonction principale pour le lancement des Hungers Games"""

        message = self.embed(self.couleur.blueColor, "E.V.E - Hunger Games", f"Chargement du module de présentation...", self.couleur.blueImageEve)
        message.format.add_field(name="Phase 1", value="*Bienvenue, bienvenue, bienvenue ! Joyeux Hunger Games et, puisse le sort vous être favorable ! Bien, avant de commencer, nous allons vous rappelez le principe des Hunger Games. Chacun des 12 districts offrira 2 tributs qui s'affronteront pour un combat à mort dans une épreuve exigeant honneur, courage et sacrifice. L'unique vainqueur, couvert de richesse, rappellera à tous, à quel point le Capitol est généreux. Ainsi nous nous remémorons notre passé, ainsi nous sauvegardons notre avenir.*")
        message.format.set_image(url='https://media.giphy.com/media/14cjnSCA3WgFLW/giphy.gif')
        await ctx.channel.send(content=None, embed=message.format)
        await asyncio.sleep(5)
        await district(self, ctx)


async def district(self, ctx, i = 1):
    """ Classe définissant et annonçant les différents district """

    districts = list()
    participants = list()

    for member in ctx.guild.members:
        if member.status in [discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]:
            participants.append(member)

    participants = random.sample(participants, k=len(participants))
    self.districts[ctx.channel.id] = []
    while i < 24 and i < len(participants):
        self.districts[ctx.channel.id].append([participants[i-1], participants[i]])
        i += 2

    participants = participants[0:i-1]

    i = 0
    district_info = self.embed(self.couleur.blueColor, "E.V.E - Hunger Games", "À présent, l'heure est venue de sélectionner les 2 courageux tributs de chaque district.", self.couleur.blueImageEve)
    for district in self.districts[ctx.channel.id]:
        district_info.format.add_field(name=f"District n°{i+1} :", value=f"{self.districts[ctx.channel.id][i][0].mention} et {self.districts[ctx.channel.id][i][1].mention}")
        i += 1

    district_info.format.set_image(url='https://media.giphy.com/media/10MnoqP5ETT8Pe/giphy.gif')
    await ctx.channel.send(content=None, embed=district_info.format)
    await asyncio.sleep(5)
    await arena_choice(self, ctx, participants)

async def arena_choice(self, ctx, participants):
    """ Fonction choisissant et annonçant l'arène qui va être utilisé durant la partie """

    arena = random.sample(self.arena, k=5)
    arena_info = self.embed(self.couleur.blueColor, "E.V.E - Hunger Games", "*Dans un instants tous les tributs vont s'affronter dans cette 73ème édition des Hunger Games. Mais avant toute chose, n'êtes-vous pas impatient de savoir dans quelle arène ils vont combattre ?!*", self.couleur.blueImageEve)
    arena_info.format.add_field(name="Tirage au sort de l'arène", value=f"*Cette année, ce sera l'arène {arena[0].biome}, n'est-ce pas fantastique ! On peut s'attendre à beaucoup de rebondissement dans ce genre d'arène !*")
    arena_info.format.set_image(url='https://media.giphy.com/media/aPLviFa7zxtdu/giphy.gif')
    await ctx.channel.send(content=None, embed=arena_info.format)
    await asyncio.sleep(1)
    await scheduler(self, ctx, arena[0], participants)

async def scheduler(self, ctx, arena, participants, day=1):
    """ Fonction principal permettant le déroulement de la partie jusqu'à sa fin """

    while len(participants) > 1:
        day_info = self.embed(self.couleur.blueColor, f"E.V.E - Hunger Games - Jour n°{day}", f"Ce message s'adresse à l'ensemble des tributs, c'est le début du jour n°{day}.", self.couleur.blueImageEve)
        await ctx.channel.send(content=None, embed=day_info.format)

        limit = 3
        if len(participants) <= 3:
            limit = len(participants)-1
        number_of_murder = random.randint(1,limit)
        for loop in range(number_of_murder):
            participants = await murder(self, ctx, arena, participants)
            await asyncio.sleep(5)

        if random.randint(0,1):
            max = len(participants)-1
            if max > 1:
                participants = await event(self, ctx, arena, participants, max)

        day += 1

    return await winner(self, ctx, participants[0])

async def murder(self, ctx, arena, participants):
    """ Fonction annonçant l'assassinat d'un tribut """

    killed, killer = random.sample(participants, k=2)
    final_death = random.sample(arena.weapons, k=1)[0]
    participants.remove(killed)

    death_info = self.embed(self.couleur.redColor, "E.V.E - Hunger Games - Mort d'un tribut !", f"Nous vous informons que {killed.mention} {final_death} {killer.mention}.", killed.avatar_url)
    death_info.format.set_image(url='https://media.giphy.com/media/NNahRR1zcqcmI/giphy.gif')
    await ctx.channel.send(content=None, embed=death_info.format)

    return participants


async def event(self, ctx, arena, participants, max):
    """ Fonction annonçant une action ou un événement durant la partie """

    v = ""
    i = random.randint(2,max)
    victims = random.sample(participants, k=i)
    for victim in victims:
        v += f"{victim.mention},"
        participants.remove(victim)

    event_type = random.sample([arena.animals, arena.traps], k=1)[0]
    final_event = random.sample(event_type, k=1)[0]
    event_info = self.embed(self.couleur.redColor, "E.V.E - Hunger Games - Evenement !", f"Cette arène contient beaucoup de piège et d'animaux, actuellement {v} {final_event}.", self.couleur.blueImageEve)
    event_info.format.set_image(url='https://media.giphy.com/media/Wo1n0QPupJHWw/giphy.gif')
    await ctx.channel.send(content=None, embed=event_info.format)

    return participants


async def winner(self, ctx, participant):
    """ Fonction annonçant la victoire d'un tribut, ceci marque la fin de la partie """
    message = self.embed(self.couleur.blueColor, "E.V.E - Hunger Games - Vainqueur", f"Mesdames et Messieurs, j'ai l'honneur de vous annoncer que {participant.mention} est le vainqueur des 73 ème Hunger Games !", self.couleur.blueImageEve)
    message.format.set_image(url='https://media.giphy.com/media/IY15PX3yCei7m/giphy.gif')
    await ctx.channel.send(content=None, embed=message.format)

def setup(eve):
    eve.add_cog(HungerGames(eve))