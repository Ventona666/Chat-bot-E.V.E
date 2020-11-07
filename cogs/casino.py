import random
import discord
from discord.ext import commands
from cogs.affichage import embed
from cogs.affichage import couleur


class Casino(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.command()
    async def slot(self, ctx, bet):
        # Fonction permettant de jouer avec une machine à sous

        author_id = ctx.author.id
        guild_id = ctx.guild.id

        self.eve.cur.execute(f"SELECT money FROM users WHERE user_id='{author_id}' AND guild_id='{guild_id}'")
        money = self.eve.cur.fetchone()[0]
        test = False

        try:
            bet = int(bet)
            included = bet >= 50 and bet <= 500
            test = True
        except:
            message = embed.Embed(self.couleur.redColor, "Casino OMEGA - E.V.E", "La mise saisie n'est pas valide", self.couleur.redImageEve)
            message.format.add_field(name="Chargement du rapport...", value=f"La mise '{bet}' que vous avez saisi comme mise n'est pas valide, veuillez entrer une mise comprise entre 50 :euro: et 100 :euro: .")
            await ctx.channel.send(content=None, embed=message.format)

        if test:
            if not included:
                message = embed.Embed(self.couleur.redColor, "Casino OMEGA - E.V.E", "La mise saisie n'est pas valide", self.couleur.redImageEve)
                message.format.add_field(name="Chargement du rapport...", value=f"Vous avez misez la somme de {bet} :euro: comme mise, or vous devez saisir une mise comprise entre 50 :euro: et 500 :euro: .")
                await ctx.channel.send(content=None, embed=message.format)

            elif money < bet:
                message = embed.Embed(self.couleur.redColor, "Casino OMEGA - E.V.E", "Vous n'avez pas assez d'argent !", self.couleur.redImageEve)
                message.format.add_field(name="Chargement du rapport...", value=f"Je ne peux accéder à votre demande, vous n'avez que {money} :euro: sur votre compte alors que vous avez misé {bet} :euro: .", inline=False)
                await ctx.channel.send(content=None, embed=message.format)

            else:
                icon_list = [(":cherries:", 25), (":kiwi:", 50), (":grapes:", 75), (":pineapple:", 100), (":coconut:", 150), (":moneybag:", 2500), (":gem:", 5000)]

                icon_1, mult_1 = random.choice(icon_list)
                icon_2, mult_2 = random.choice(icon_list)
                icon_3, mult_3 = random.choice(icon_list)

                total_mult = mult_1 + mult_2 + mult_3

                message = embed.Embed(self.couleur.blueColor, "Casino OMEGA - E.V.E", "Machine à sous", self.couleur.blueImageEve)
                message.format.add_field(name="Puisse le sort vous être favorable !", value=f"== {icon_1} | {icon_2} | {icon_3} ==", inline=False)

                if icon_1 == icon_2 and icon_2 == icon_3:
                    gain = bet * mult_1
                    message.format.add_field(name="Module de félicitation en cours de chargement...", value=f"Incroyable, vous avez gagnez et remportez ainsi la somme de {gain} :euro:")

                elif ":gem:" in [icon_1, icon_2, icon_3] and total_mult <= 10000:
                    gain = bet // 2
                    message.format.add_field(name="Vous n'avez pas tout perdu !", value=f"Il y a 1 diamant ! Vous repartez avec la moitié de votre mise, soit {gain} :euro: !")

                elif ":gem:" in [icon_1, icon_2, icon_3] and total_mult > 10000 and total_mult <= 12500:
                    gain = bet
                    message.format.add_field(name="Pas si mal !", value=f"Il y a 2 diamants ! Vous remportez votre mise de départ, soit {gain} :euro: !")
                else:
                    gain = 0
                    message.format.add_field(name="Dommage !", value=f"Vous n'avez pas eu de chance, vous ne gagnez aucun gain !")

                self.eve.cur.execute(f"UPDATE users SET money = money-{bet}+{gain} WHERE user_id='{author_id}' AND guild_id='{guild_id}'")
                self.eve.conn.commit()

                await ctx.channel.send(content=None, embed=message.format)

    @commands.command()
    async def roulette(self, ctx, number, bet):
        # Fonction permettant de jouer à la roulette
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        test = await test_roulette(self, ctx, number, bet)
        number = int(number)
        bet = int(bet)
        message = embed.Embed(self.couleur.blueColor, "Casino OMEGA - E.V.E", "Roulette", self.couleur.blueImageEve)

        if test:
            winning_number = random.randint(0,49)
            if winning_number == number:
                gain = bet * 50
                message.format.add_field(name="Module de félicitation en cours de chargement...", value=f"Le nombre gagnant est {winning_number} ! Incroyable, vous avez gagnez et remportez ainsi la somme de {gain} :euro:")

            elif winning_number % 2 == number % 2:
                gain = bet // 2
                message.format.add_field(name="Vous n'avez pas tout perdu !", value=f"Le nombre gagnant est {winning_number}, c'est la même couleur que {number} ! Vous repartez avec la moitié de votre mise, soit {gain} :euro:")
            else:
                gain = 0
                message.format.add_field(name="Dommage !", value=f"Le numéro gagnant est {winning_number}. Vous n'avez pas eu de chance, vous ne gagnez aucun gain !")

            self.eve.cur.execute(f"UPDATE users SET money = money-{bet}+{gain} WHERE user_id='{author_id}' AND guild_id='{guild_id}'")
            self.eve.conn.commit()
            await ctx.channel.send(content=None, embed=message.format)


async def test_roulette(self, ctx, number, bet):
    check = True
    error = embed.Embed(self.couleur.redColor, "Casino OMEGA - Roulette - E.V.E", "Erreur dans la commande", self.couleur.redImageEve)

    try:
        number = int(number)
        number_included = number >= 0 and number <= 49
    except:
        error.format.add_field(name="Numéro invalide", value=f"La valeur '{number}' n'est pas nombre, or vous devez saisir un nombre sur lequel miser.")
        check = False

    try:
        bet = int(bet)
        bet_included = bet >= 50 and bet <= 500
    except:
        error.format.add_field(name="Mise invalide", value=f"La valeur '{bet}' n'est pas nombre, or vous devez saisir une mise.", inline=False)
        check = False

    if not check:
        await ctx.channel.send(content=None, embed=error.format)
        return False

    elif not number_included:
        error.format.add_field(name="Numéro invalide", value=f"Vous avez misez sur le numéro {number}, or vous devez saisir un numéro entre 0 et 49.", inline=False)
        await ctx.channel.send(content=None, embed=error.format)
        return False

    elif not bet_included:
        error.format.add_field(name="Mise invalide", value=f"Vous avez misez la somme de {bet} :euro: comme mise, or vous devez saisir une mise comprise entre 50 :euro: et 500 :euro: .", inline=False)
        await ctx.channel.send(content=None, embed=error.format)
        return False
    return True

def setup(eve):
    eve.add_cog(Casino(eve))