import discord
import requests
from broker import broker_json
from runes import runes_json
from datetime import datetime
from runes import rune_weight
from runes import rune_name
from discord_ui.broker import broker_embed
from discord_ui.broker import broker_button
from discord_ui.runes import runes_button


async def broke(interaction: discord.Interaction, item_id: str):
    await interaction.response.defer()
    full_url = f"https://api.dofusdu.de/dofus2/fr/items/equipment/{item_id}"
    try:
        # Effectuer la requête GET à l'API
        response = requests.get(full_url)

        # Vérifier si la requête a réussi (code 200)
        if response.status_code == 200:

            # Convertir la réponse API en JSON  && Récupérer les donnée Local
            data = response.json()
            coef, coef_last_update = broker_json.get_element_info(item_id)

            item_lvl = data['level']

            # Créer l'ui
            view = discord.ui.View(timeout=None)
            embed = broker_embed.ItemBrokerEmbed(item_name=data['name'], item_lvl= item_lvl, thumbnail_url=data['image_urls']['sd'])
            embed.add_coeff_info(coef= coef, last_update = coef_last_update)
            
            if(coef != None):

                coef_float = float(coef)

                rune_id_list= []
                rune_weight_list = []

                # Parcourir chaque stat de l'item dans ['effects'] et on les rajoute dans notre liste a traiter
                for item in data['effects']:

                    if item['type']['is_active'] == False:
                        if item['type']['id'] in rune_weight.caracteristiques:

                            weight_value = rune_weight.caracteristiques[item['type']['id']]
                            print(f"Weight value rune {item['type']['id']} : {weight_value}")
                            if item['int_maximum'] != 0:
                                jet = (item['int_minimum'] + item['int_maximum']) / 2

                            else:
                                jet = item['int_minimum']
                            
                            stats_weight = (3 * jet * weight_value * item_lvl / 200 + 1)
                            
                            if stats_weight < 0:
                                stats_weight = stats_weight / 5
                                print("Pourquoi je passe")
                            
                            rune_id_list.append(item['type']['id'])
                            rune_weight_list.append(stats_weight)

                #Sauvegarde le nombre de runes si il y a focus
                rune_focus_list = []

                # Parcourir chaque élément de l'array
                for i in range(len(rune_id_list)):

                    current_stats = rune_weight_list[i]
                    
                    # Calculer la somme de toutes les autres valeurs (sauf l'élément actuel)
                    sum_of_other_items = sum([item for j, item in enumerate(rune_weight_list) if j != i])
                    
                    amount_focus_rune = current_stats + 0.5 * sum_of_other_items
                    # Ajouter le résultat final à la liste
                    rune_focus_list.append(amount_focus_rune)
                
                nofocus_total_kamas = 0
                name_most_profitable_rune = None
                max_profit = 0

                for h in range(len(rune_id_list)):
                    

                    #On skip les stats a afficher et focus sur discord
                    if rune_weight_list[h] < 0:
                        continue

                    current_ID = rune_id_list[h]
                    rune_price, update_older_than_12h = runes_json.get_rune_price(current_ID)

                    #Chasse
                    if current_ID == 92:
                        continue
                    #Vita
                    elif current_ID == 9:
                        divisor = 1
                    #Ini
                    elif current_ID == 24:
                        divisor = 1
                    #Pods
                    elif current_ID == 78:
                        divisor = 2.5                        
                    else:
                        print(f"{current_ID} Je passe")
                        divisor = rune_weight.caracteristiques[current_ID]


                    quantity_nofocus_rune = round(rune_weight_list[h] * coef_float / 100 / divisor, 2)
                    nofocus_amount_kamas = int(quantity_nofocus_rune * rune_price)
                    nofocus_total_kamas += nofocus_amount_kamas

                    quantity_focus_rune = round(rune_focus_list[h] * coef_float / 100 / divisor, 2)
                    focus_amount_kamas = int(quantity_focus_rune * rune_price)

                    if max_profit < focus_amount_kamas:
                        max_profit = focus_amount_kamas
                        name_most_profitable_rune = rune_name.runes_name[current_ID]

                    embed.add_stat_info(
                        rune_name = rune_name.runes_name[current_ID], 
                        rune_price= rune_price,
                        quantity_nofocus_rune = quantity_nofocus_rune,
                        nofocus_amount_kamas = nofocus_amount_kamas,
                        quantity_focus_rune = quantity_focus_rune,
                        focus_amount_kamas = focus_amount_kamas,
                        update_older_than_12h = update_older_than_12h
                        )

                embed.add_conseil_focus(
                    nofocus_total_kamas = nofocus_total_kamas,
                    max_profit=max_profit, 
                    name_most_profitable_rune =name_most_profitable_rune)
                 

                changepriceselection = runes_button.ButtonSelectionRune(data_id=rune_id_list, label="Modifier Prix Rune", ankama_id=item_id)
                view.add_item(changepriceselection)


            # Créer une vue (View) avec le bouton
            button = broker_button.ModificationCoefButton(label=f"Modifier Coeff", item_name=data['name'], ankama_id=item_id)
            view.add_item(button)
            
            view.add_item(broker_button.AddFavoriteButton(ankama_id=item_id))
            view.add_item(broker_button.HelpButton())

            # Envoyer l'embed avec la vue
            await interaction.followup.send(embed=embed, view=view, ephemeral=True, content="*Le nombre de runes ainsi que le Gain Estimé sont calculés en fonction des statistiques moyennes de l'équipement. Vous pouvez obtenir plus ou moins de runes en fonction du jet.*\n Merci de mettre à jour le coefficient une fois que vous avez terminé vos brisages 😉")
        else:
            # En cas d'erreur, envoyer un message avec le code d'erreur
            await interaction.followup.send(f"Erreur de la requête : {response.status_code}")
    except Exception as e:
        # Gérer les exceptions, par exemple, envoyer un message avec l'erreur
        await interaction.followup.send(f"Une erreur s'est produite : {e}")