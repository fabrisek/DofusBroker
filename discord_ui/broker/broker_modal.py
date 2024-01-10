import discord
from broker import broker_json
from broker import broker_main

class ModifCoefModal(discord.ui.Modal):
    def __init__(self, item_name, ankama_id):
        super().__init__(title="Modifier le Coeff de l'item")
        self.item_name = item_name
        self.ankama_id = ankama_id

    name = discord.ui.TextInput(
        label=f'Nouveau % de l\'item :',
        placeholder='Exemple : 182',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_value = float(self.name.value)
            if 0 <= new_value <= 4000:
                broker_json.update_coefficient(self.ankama_id, self.name.value)
                await broker_main.broke(interaction, self.ankama_id)
            else:
                await interaction.response.send_message('Please enter a number between 0 and 4000.', ephemeral=True)
        except ValueError:
            await interaction.response.send_message('Please enter a valid number.', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.' + error, ephemeral=True)

