import discord
from discord_ui.runes import runes_select

class ButtonSelectionRune(discord.ui.Button):
    def __init__(self, label, data_id, ankama_id):
            super().__init__(style=discord.ButtonStyle.green, label=label, emoji="💵")
            self.data_id = data_id
            self.ankama_id = ankama_id

    async def callback(self, interaction: discord.Interaction):
        view = discord.ui.View()
        dropdown = runes_select.Dropdown(data_id=self.data_id, ankama_id=self.ankama_id)
        view.add_item(dropdown)
        await interaction.response.send_message(content="Choisissez le prix d'une rune à modifié", view=view)

