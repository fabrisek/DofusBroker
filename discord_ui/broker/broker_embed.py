import discord

class ItemBrokerEmbed(discord.Embed):    
    def __init__(self, item_name, item_lvl, thumbnail_url):
        super().__init__(title= item_name, description=f"Niveau : {item_lvl}")
        self.item_name = item_name
        super().set_thumbnail(url=thumbnail_url)

        super().set_footer(text="❌= Sans Focus | 🧲 = Avec Focus | ⚠️ = Dernier Prix Actualisé > 12h")

    def add_conseil_focus(self, nofocus_total_kamas, max_profit, name_most_profitable_rune):

        if nofocus_total_kamas > max_profit:
            super().add_field(name="CONSEIL FOCUS :", value= f"\n~\n**AUCUN FOCUS** | Gain Estimé : **{nofocus_total_kamas}** Kamas\n~", inline=False)
        else:
            super().add_field(name="CONSEIL FOCUS :", value= f"\n~\n**{name_most_profitable_rune}** | Gain Estimé : **{max_profit}** Kamas\n~", inline=False)

    def add_stat_info(self, rune_name, rune_price, quantity_focus_rune, focus_amount_kamas, quantity_nofocus_rune, nofocus_amount_kamas,update_older_than_12h):
        rune_price_str = str(rune_price)
        final_name = rune_name + " ( "

        if update_older_than_12h == True:
            final_name += "⚠️ "

        final_name += rune_price_str + " K /u ) :"

        field_content = f"\n \n❌ {quantity_nofocus_rune} | {nofocus_amount_kamas} Kamas \n\n 🧲 {quantity_focus_rune} | {focus_amount_kamas} Kamas\n---------------------" 
        super().add_field(name=final_name , value=field_content, inline=False)


    def add_coeff_info(self, coef, last_update):
        
        if coef != None : 
            super().add_field(name="Dernier Brisage :", value= last_update, inline=True)
            super().add_field(name="Coefficient :", value=coef + " % ", inline=True)
            super().add_field(name=" ", value=" ", inline=False)
        else: 
            super().add_field(name="Dernier Brisage :", value= "N/A", inline=True)
            super().add_field(name="Coefficient :", value= "N/A", inline=True)
            super().add_field(name="⚠️❗️ ERROR ❗️⚠️", value= "**AUCUNE DATA RELATIVE A CET OBJET, VEUILLEZ METTRE A JOUR LE COEFF**",inline=False)