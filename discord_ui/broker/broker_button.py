import discord
from discord_ui.broker import broker_modal

class ModificationCoefButton(discord.ui.Button):
    def __init__(self, label, item_name, ankama_id):
        super().__init__(style=discord.ButtonStyle.green, label=label, emoji="🎲")
        self.item_name = item_name
        self.ankama_id = ankama_id

    async def callback(self, interaction: discord.Interaction):

        try:     
            await interaction.response.send_modal(broker_modal.ModifCoefModal(item_name=self.item_name, ankama_id=self.ankama_id))

        except Exception as e:
            print(f"Erreur dans le callback : {e}")

class HelpButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label="Help ?", emoji="❓",row=2)

    async def callback(self, interaction: discord.Interaction):
                
        await interaction.response.send_message(content="Help Message", ephemeral=True)

class AddFavoriteButton(discord.ui.Button):
    def __init__(self, ankama_id):
        super().__init__(style=discord.ButtonStyle.primary, label="Ajouter Favoris", emoji="⭐",row=2)
        self.ankama_id = ankama_id

    async def callback(self, interaction: discord.Interaction):
                
        await interaction.response.send_message(content="Favori Message", ephemeral=True)