import discord
from runes import runes_json
from broker import broker_main

class ModifRuneModal(discord.ui.Modal):
    def __init__(self, rune_id, ankama_id):
        super().__init__(title="Modifier le prix d'une Rune", timeout=None)
        self.rune_id = rune_id
        self.ankama_id = ankama_id

    price = discord.ui.TextInput(
        label='Nouveau prix moyen de la rune :',
        placeholder='Exemple : 182',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_value = float(self.price.value)
            runes_json.modify_rune_price(rune_id= self.rune_id, new_price= new_value)
            await broker_main.broke(interaction, self.ankama_id)

        except ValueError:
            await interaction.response.send_message('Please enter a valid number.', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.' + error, ephemeral=True)