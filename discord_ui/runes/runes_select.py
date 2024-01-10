import discord
from discord_ui.runes import runes_modal
from runes import rune_name
from runes import runes_json
class Dropdown(discord.ui.Select):
    def __init__(self, data_id, ankama_id):
        super().__init__(placeholder="Selectionez une Rune")
        self.ankama_id = ankama_id
        self.data_id = data_id
        
        for i in range(len(self.data_id)):
            rune_price ,lastdate = runes_json.get_rune_price(data_id[i])
            option = discord.SelectOption(label=rune_name.runes_name[data_id[i]], description=f"Prix Moyen Actuel : {rune_price} K/u", value=self.data_id[i])
            self.append_option(option)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(runes_modal.ModifRuneModal(rune_id=self.values[0], ankama_id=self.ankama_id))