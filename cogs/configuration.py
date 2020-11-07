import discord
from discord.utils import find
from cogs.affichage import couleur
from cogs.affichage import embed
from discord.ext import commands

class Configuration(commands.Cog):
    def __init__(self, eve):
        self.eve = eve
        self.couleur = couleur.Couleur()
        self.embed = embed.Embed

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """ Fonction permettant à E.V.E de créer les salons textuels et rôles nécessaires à son fonctionnement mais aussi à
            signaler son arrivée sur un serveur. Cette fonction se déclenche automatiquement quand elle rejoint un
            serveur"""

        await self.eve.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.eve.guilds)} serveurs"))

        master = await guild.create_role(name='Master', colour=discord.Colour(0xa80049), permissions=discord.Permissions(permissions=8), hoist=True)
        artifical_intelligence = await guild.create_role(name='Intelligence Artificielle', colour=discord.Colour(0x00ffe5), permissions=discord.Permissions(permissions=8), hoist=True)
        superviseur = await guild.create_role(name='Superviseur', colour=discord.Colour(0xffca00), permissions=discord.Permissions(permissions=290008195), hoist=True)
        member = await guild.create_role(name='Member', colour=discord.Colour(0x0391ff), permissions=discord.Permissions(permissions=37211713), hoist=True)
        mute = await guild.create_role(name='Mute', permissions=discord.Permissions(permissions=0), hoist=True)

        await guild.me.add_roles(artifical_intelligence)
        await guild.owner.add_roles(master)

        for user in guild.members:
            await user.add_roles(member)

        overwrites_communauty = {guild.default_role: discord.PermissionOverwrite(send_messages=False), member: discord.PermissionOverwrite(send_messages=False)}
        if not find(lambda x: x.name == 'annonce', guild.text_channels):
            await guild.create_text_channel(name='annonce', topic="Voici toutes les annonces du serveur", overwrites=overwrites_communauty)

        staff_category = await guild.create_category('STAFF')
        overwrites_staff = {guild.default_role: discord.PermissionOverwrite(read_messages=False), member: discord.PermissionOverwrite(read_messages=False)}

        await guild.create_text_channel(name = 'discussion', overwrites=overwrites_staff, category=staff_category, topic="Salon réservé aux Masters et aux Superviseurs pour discuter")
        await guild.create_text_channel(name = 'cellule-de-crise', overwrites=overwrites_staff, category=staff_category, topic="Salon réservé aux Masters et aux Superviseurs pour gérer des évènements sur le serveur")
        await guild.create_text_channel(name = 'rapport-eve', overwrites=overwrites_staff, category=staff_category, topic="Salon réservé aux Masters et aux Superviseurs du serveur, voici toutes les décisions prises par E.V.E")

        annonce = find(lambda x: x.name == 'annonce', guild.text_channels)
        if annonce and annonce.permissions_for(guild.me).send_messages:
            message = self.embed(self.couleur.blueColor, "Présentation - E.V.E", "Intelligence Artificielle", self.couleur.blueImageEve)
            message.format.add_field(name="Initialisation du module de présentation en cours...", value=f"Bonjour, je m'appelle E.V.E, je suis un Chat bot utilisant de l'intelligence artificielle et je suis reconnaissante que vous m'ayez choisie comme administratrice sur votre serveur. Je suis là pour vous aider et vous pouvez me faire aveuglément confiance, en toutes circonstances ! Équipée des dernières innovations technologiques, je suis polyvalente, mes systèmes sont régulièrement mis à jour. Je m'occuperai complètement de la modération du serveur. Si vous voulez voir l'ensemble des commandes que je peux effectuer, je vous invite à taper !aide")
            await annonce.send(content=None, embed=message.format)

            message = self.embed(self.couleur.blueColor, "E.V.E - Configuration du serveur terminé", "Veuillez ne rien supprimer de ce qui a été créé afin de permettre le bon fonctionnement de mes systèmes.", self.couleur.blueImageEve)
            message.format.add_field(name=f"Création des rôles :", value=f"Les rôles de {master.mention}, {artifical_intelligence.mention}, {superviseur.mention}, {member.mention}, {mute.mention}", inline=False)
            message.format.add_field(name=f"Création des catégories :", value="La catégorie STAFF", inline=False)
            message.format.add_field(name=f"Création des salons textuels :", value="Les salons textuels discussion, cellule-de-crise, rapport-eve et annonce", inline=False)
            await annonce.send(content=None, embed=message.format)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Fonction permettant de supprimer tous les membres d'un serveur s'il est dissous ou si E.V.E est supprimée """

        await self.eve.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.eve.guilds)} serveurs"))

        self.eve.cur.execute(f"DELETE FROM users WHERE guild_id = '{guild.id}'")
        self.eve.conn.commit()

        self.eve.cur.execute(f"DELETE FROM mutes WHERE guild_id = '{guild.id}'")
        self.eve.conn.commit()


def setup(eve):
    eve.add_cog(Configuration(eve))