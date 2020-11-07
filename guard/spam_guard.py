# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# Anti-spam for discord server.
#
# (C) 2020 Tony De Freitas, Toulouse, France
# Released under GNU Affero General Public License v3.0 (AGPLv3)
# email defreitas.tony.pro@gmail.com
# -----------------------------------------------------------

from datetime import datetime
from discord.utils import get
from cogs import security
from logs import logs

async def anti_spam(self, author_id, guild_id, ctx):
    """ Fonction empêchant le spam d'un chat, vérifie plusieurs paramètres, à savoir :
        - L'auteur des messages
        - Le nombre de messages envoyés par l'auteur en question
        - Le temps écoulé entre chaque message """

    def _check(m):
        return str(m.author.id) == author_id and (datetime.utcnow()-m.created_at).seconds < 10

    spam = list(filter(lambda m: _check(m), self.eve.cached_messages))

    if len(spam) > 3:
        await ctx.channel.delete_messages(spam)

        self.eve.cur.execute(f"UPDATE users SET offense=offense+1 WHERE user_id = '{author_id}' AND guild_id = '{guild_id}'")
        self.eve.conn.commit()

        if not get(ctx.guild.roles, name="Mute") in ctx.author.roles:
            await logs.member_log(self, ctx.author, "Mute", "Vous avez envoyé beaucoup de message durant un cours lapse de temps, par mesure de précaution, je vous mute temporairement.", None, 5)
            await security.mute(self, ctx.author, ctx.guild, 300)