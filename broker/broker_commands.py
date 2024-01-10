import discord
from discord.ext import commands
from discord import app_commands
import requests
from broker import broker_main

class SearchItemButton(discord.ui.Button):
    def __init__(self, label, item_name, ankama_id):
        super().__init__(style=discord.ButtonStyle.primary, label=label)
        self.item_name = item_name
        self.ankama_id = ankama_id

    async def callback(self, interaction: discord.Interaction):
        # Vous pouvez ajouter ici le code que vous souhaitez exécuter lorsque le bouton est cliqué
        await broker_main.broke(interaction= interaction, item_id=self.ankama_id)


class BrokerCommands(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
        self.api_url = "https://api.dofusdu.de/dofus2/fr/items/equipment/search"


    @app_commands.command(description='Runes Broker', name="search")
    async def search(self, interaction: discord.Interaction, item_name: str):
        await interaction.response.defer(ephemeral=True)
        full_url = f"{self.api_url}?query={item_name}&limit=5"
        print(full_url)
        try:
            # Effectuer la requête GET à l'API
            response = requests.get(full_url)

            # Vérifier si la requête a réussi (code 200)
            if response.status_code == 200:
                # Convertir la réponse en JSON
                data = response.json()
                for item in data:

                    if item['type']['name'] == "Dofus":
                        continue

                    # Créer un nouvel embed
                    embed = discord.Embed(title=f"{item['name']}")
                    embed.add_field(name="Catégorie :", value=item['type']['name'], inline=True)
                    embed.add_field(name="Level :", value=item['level'], inline=True)
                    embed.set_thumbnail(url=item['image_urls']['sd'])
# Créer un bouton avec le nom de l'élément
                    button = SearchItemButton(label=f"Voir plus...", item_name=item['name'], ankama_id=item['ankama_id'])

                    # Créer une vue (View) avec le bouton
                    view = discord.ui.View()
                    view.add_item(button)

                    # Envoyer l'embed avec la vue
                    await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            else:
                # En cas d'erreur, envoyer un message avec le code d'erreur
                await interaction.followup.send(f"Erreur de la requête : {response.status_code}")
        except Exception as e:
            # Gérer les exceptions, par exemple, envoyer un message avec l'erreur
            await interaction.followup.send(f"Une erreur s'est produite : {e}")

