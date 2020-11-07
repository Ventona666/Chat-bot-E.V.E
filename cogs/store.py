# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Store for discord server
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------


import os
import time
import json
import random
import asyncio
import discord
import requests
import bs4 as bs
import urllib.request
from datetime import datetime
from discord.utils import get
from discord.utils import find
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur


class Items:
    """ Classe définissant les caractéristiques d'un objet du store OMEGA, à savoir :
        - Le nom
        - La commande
        - La description
        - Le prix """

    def __init__(self, name, command, description, price, bar_code):
        self.name = name
        self.command = command
        self.description = description
        self.price = price
        self.bar_code = bar_code


class Store(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed
        self.inventory = [Items("Service de nettoyage :soap:", "!sponge", "Vous avez dit quelque chose qu'il ne fallait pas ? Laissez moi faire, je fais disparaître votre dernier message.", "20", 100),
                          Items("Service d'embeding :diamond_shape_with_a_dot_inside:", "!embed (titre / texte)", "Vous voulez rendre votre message aussi agréable à regarder que les miens ? Je m'en occupe !", "30", 101),
                          Items("Bulletin météorologique :white_sun_rain_cloud:", "!meteo (nom de la ville)", "Je vous envoie en message privé la météo de la ville souhaitée.", "50", 102),
                          Items("Recherche Wikipedia :mag_right:", "!wiki (ce que vous voulez rechercher)", "Je vais chercher l'information souhaitée sur Wikipedia.", "100", 103),
                          Items("Gif animé :smiling_face_with_3_hearts:", "!gif (ce que vous cherchez)", "Je cherche et je vous envoie d'un gif animé.", "100", 200),
                          Items("Corruption de la base de donnée :credit_card:", "!corruption", "Toutes les infractions que vous avez comises sont effacées de ma base de donnée.", "10000", 300)]


    def convert(argument):
        """ Fonction qui remplace les espaces d'une chaine de caractère par des '+', cela permet d'avoir un format
            valide pour les requêtes dans un url. """

        return argument.replace(" ", "+")


    def separator(argument):
        """ Fonction permettant repérer les '/' dans une chaine de caractères et de renvoyer une liste composée
            des éléments de la chaine de caractère séparés par les '/'. """

        argument = argument.split()
        last_argument = len(argument)-1
        text, elements = list(), list()
        i = 0

        while i < len(argument):
            sep = argument[i] == '/'
            if not sep:
                text.append(argument[i])
            if sep or i == last_argument:
                text = " ".join(text)
                elements.append(text)
                text = list()
            i += 1

        return elements


    @commands.command()
    async def store(self, ctx):
        """ Affiche tout les articles disponibles dans le store OMEGA ainsi que les crédits possédés par l'utilisateur """

        self.eve.cur.execute(f"SELECT money FROM users WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}'")
        money = self.eve.cur.fetchone()[0]

        message = self.embed(self.couleur.blueColor, "Store OMEGA - E.V.E", f"Bienvenue {ctx.author.mention} au Store OMEGA. Vous y trouvez plusieurs fonctions en échange des crédits que vous avez accumulé depuis votre arrivée sur le serveur.", self.couleur.blueImageEve)
        message.format.add_field(name="Votre compte bancaire", value=f"Vous avez {money} :euro:.", inline=False)

        for item in self.inventory:
            message.format.add_field(name=item.name + "\nCommande : " + "`" + item.command + "`", value= "*" + item.description + "*" + "\n__Prix__ : " + item.price + "  :euro:", inline=False)

        await ctx.channel.send(content=None, embed=message.format)


    @commands.command()
    async def sponge(self, ctx):
        """ Fonction permettant d'effacer le dernier message de l'utilisateur """

        if await payment(self, ctx, 100):
            def _check(m):
                return str(m.author.id) == str(ctx.author.id) and (datetime.utcnow()-m.created_at).seconds < 300

            user_message = list(filter(lambda m: _check(m), self.eve.cached_messages))
            await ctx.channel.delete_messages(user_message)


    @commands.command(name="embed")
    async def embeding(self, ctx, *, elements : separator):
        """ Fonction permettant de transformer un message simple en embed """

        if await payment(self, ctx, 101):
            await ctx.channel.purge(limit=1)
            msg = self.embed(self.couleur.blueColor, f"{ctx.author} - {elements[0]}", elements[1], ctx.author.avatar_url)
            await ctx.send(content=None, embed=msg.format)


    @commands.command(name="meteo")
    async def weather(self, ctx, *, city_name):
        """ Fonction envoyant en message privé la météo de la ville souhaitée """

        if await payment(self, ctx, 102):
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=4bdbc58140e01c04c9ff16a3a84a594b'
            content = requests.get(url)
            data = content.json()

            with open('cogs\data\weather.json', 'r', encoding='utf-8') as f:
                weather_condition = json.load(f)
                f.close()

            id = str(data['weather'][0]['id'])
            icon = weather_condition[id][0]
            text = weather_condition[id][1]
            temp = data['main']['temp']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            country = data['sys']['country']
            wind = data['wind']['speed']

            weather_report = self.embed(self.couleur.blueColor, f"E.V.E - Météo de {city_name.capitalize()}, {country}", f"Voici votre bulletin météo pour {city_name.capitalize()}, {ctx.author.mention}.", self.couleur.blueImageEve)
            weather_report.format.add_field(name=f"Météo actuelle - {icon}", value=text, inline=False)
            weather_report.format.add_field(name="Température actuelle :thermometer:", value=f"{round(temp - 273.15, 1)} °c")
            weather_report.format.add_field(name="Température minimale :cold_face:", value=f"{round(temp_min - 273.15, 1)} °c")
            weather_report.format.add_field(name="Température maximale :hot_face:", value=f"{round(temp_max - 273.15, 1)} °c")
            weather_report.format.add_field(name="Humidité :droplet:", value=f"{humidity} %")
            weather_report.format.add_field(name="Vent :wind_blowing_face:", value=f"{wind} m/s")
            weather_report.format.add_field(name="Pression", value=f"{pressure} hPa")
            await ctx.author.send(content=None, embed=weather_report.format)


    @commands.command()
    async def wiki(self, ctx, *, query : convert):
        """ Fonction envoyant en message privé les dernières actualités extrait du Figaro. """

        if await payment(self, ctx, 103):
            url = f'https://fr.wikipedia.org/wiki/Special:Search?search={query}&go=Go'
            req = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(req, 'lxml')
            title = soup.find(id="firstHeading").text

            i = 1
            content = " "
            while len(content) < 60:
                content = soup.find(id="mw-content-text").find_all("p")[i].text
                i += 1

            message = self.embed(self.couleur.blueColor, "E.V.E - Wikipedia", title, self.couleur.blueImageEve)
            message.format.add_field(name="Voici les informations relatives à votre recherche", value=content, inline=False)
            message.format.add_field(name="Voici le lien de l'article", value=url)
            await ctx.channel.send(content=None, embed=message.format)


    @commands.command()
    async def gif(self, ctx, *, query : convert):
        """ Fonction envoyant un gif animé à l'utilisateur"""

        if await payment(self, ctx, 200):
            data = json.loads(urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q={query}&api_key=QbsfQmUYP2WW9fJY6dAYEPDvmQNP8kFi&limit=25&lang=fr&rating=pg").read())
            if data['pagination']['total_count'] > 0:
                message = self.embed(self.couleur.blueColor, "E.V.E - Gif animé", f"Voici ce que vous m'avez demandé {ctx.author.mention}. ", self.couleur.blueImageEve)
                message.format.set_image(url=data['data'][random.randint(0,24)]['images']['original']['url'])
            else:
                message = self.embed(self.couleur.redColor, "E.V.E - Gif animé non trouvé", f"Toutes mes excuses {ctx.author.mention} mais je ne suis pas parvenu à trouver un gif animé correspondant à votre recherche.", self.couleur.redImageEve)
                message.format.set_image(url='https://media.giphy.com/media/cjzkCDL3jZTZB6ki1B/giphy.gif')

            await ctx.send(content=None, embed=message.format)


    @commands.command()
    async def corruption(self, ctx):
        """ Permet d'effacer toutes les infractions comises par l'utilisateur """

        if await payment(self, ctx, 300):
            self.eve.cur.execute(f"UPDATE users SET offense = 0 WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}'")
            self.eve.conn.commit()

            message = self.embed(self.couleur.blueColor, "E.V.E - Corruption", "La transaction a été acceptée", self.couleur.blueImageEve)
            message.format.add_field(name="Information", value=f"Merci pour votre achat {ctx.author.mention} ! J'ai remarqué dans ma base de donnée que vous n'avez commis aucune infraction depuis votre arrivée sur le serveur, je tiens à vous féliciter pour votre comportement exemplaire !", inline=False)
            await ctx.channel.send(content=None, embed=message.format)


async def payment(self, ctx, bar_code):
    """ Fonction permettant le paiement d'un item au store OMEGA """

    self.eve.cur.execute(f"SELECT money FROM users WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}'")
    money = self.eve.cur.fetchone()[0]
    for item in self.inventory:
        if item.bar_code == bar_code:
            item_price = int(item.price)

    if money >= item_price:
        self.eve.cur.execute(f"UPDATE users SET money = money-{item_price} WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}'")
        self.eve.conn.commit()
        return True
    else:
        await denied_payment(self, ctx, item_price, money)
        return False


async def denied_payment(self, ctx, item_price, money):
    """ Signale à l'utilisateur qu'il n'a pas assez d'argent sur son compte """

    information = self.embed(self.couleur.redColor, "E.V.E - Paiement refusé !", f"Désolé {ctx.author.mention} mais le paiement a été refusé.", self.couleur.redImageEve)
    information.format.add_field(name="Voici la raison", value=f"Malheuresement, cet item est proposé au prix de {item_price} :euro: et vous avez actuellement sur votre compte {money} :euro: ! Vous pourrez à nouveau essayer quand vous aurez accumulé assez d'argent.")
    await ctx.send(content=None, embed=information.format, delete_after=25)


def setup(eve):
    eve.add_cog(Store(eve))
