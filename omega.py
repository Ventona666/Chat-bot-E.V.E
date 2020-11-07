# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Main file to start the chat bot and connect to the data base.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

import os
import discord
import psycopg2
from discord.ext import commands
from discord.ext.commands import Bot
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True

def main():
    # Fonction principale permettant le démarrage de E.V.E et la connexion à se base de donnée

    eve = commands.Bot(command_prefix = '!', description='Je suis une IA nommée E.V.E et développée par Ventona', intents=intents)
    os.environ['DATABASE_URL'] = 'postgres://yskjiminweifna:7afbecaa63602208b3505a0064a4b9cbb7064050d30218ad2ff020fbe5972317@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d9dtp27gp6j7ba'
    DATABASE_URL = os.environ['DATABASE_URL']
    eve.conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    eve.cur = eve.conn.cursor()

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            eve.load_extension(f'cogs.{filename[:-3]}')


    eve.run('NjcyNTIxODEyMzE1NDcxODgz.XxP9Mg.sSU6RK9eq5HQllxidMJP9Qb93BE')

if __name__ == '__main__':
    main()

    eve.run('NzA5MzA2OTc3MjU1NDI0MDcx.XrkH3A.F8AKea_c6GQnmIM_sPGefr7bHpc')

main()

