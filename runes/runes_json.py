import json
from datetime import datetime

def load_runes_data():
    try:
        with open("data/rune_price.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Le fichier rune_price.json n'a pas été trouvé.")
        return {"runes": []}
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        return {"runes": []}

def save_runes_data(runes_data):
    with open("data/rune_price.json", "w", encoding="utf-8") as file:
        json.dump(runes_data, file, indent=2)

from datetime import datetime, timedelta

from datetime import datetime, timedelta

def get_rune_price(rune_id):
    runes_data = load_runes_data()
    
    for rune in runes_data["runes"]:
        if rune["rune"] == str(rune_id):
            current_price = rune["current_price"]["value"]
            update_date_str = rune["current_price"]["update_date"]

            try:
                if update_date_str is not None:
                    # Convertir la date de mise à jour en objet datetime
                    update_date = datetime.strptime(update_date_str, "%d/%m/%Y %H:%M:%S")
                    
                    # Vérifier si la mise à jour a été effectuée il y a plus de 24 heures
                    update_older_than_24h = datetime.now() - update_date > timedelta(hours=12)
                    
                    return current_price, update_older_than_24h
                else:
                    # Gérer le cas où la date de mise à jour est manquante (None)
                    print("Erreur : La date de mise à jour est manquante.")
                    return current_price, True

            except ValueError:
                # Gérer le cas où la conversion échoue (date invalide)
                print(f"Erreur : La date {update_date_str} n'est pas valide.")
                return current_price, True
    print(f"RUne pas trouve{rune_id}")
    return 0, True


# Example usage:
# Uncomment the following lines to test the functions
# modify_rune_price("PA", 50)
# get_rune_price("PA")

from datetime import datetime

def modify_rune_price(rune_id, new_price):
    runes_data = load_runes_data()
    
    for rune in runes_data["runes"]:
        if rune["rune"] == rune_id:
            old_price = rune["current_price"]["value"]
            old_update_date = rune["current_price"]["update_date"]           
            rune["current_price"]["value"] = new_price
            rune["current_price"]["update_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            if old_price is not None and old_update_date is not None:
                rune["previous_prices"].append({
                    "value": old_price,
                    "update_date": old_update_date
                })
            
            save_runes_data(runes_data)  # Sauvegarde après la modification
            return True
    
    # Si la rune n'existe pas, on la crée
    new_rune = {
        "rune": rune_id,
        "current_price": {
            "value": new_price,
            "update_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        },
        "previous_prices": []
    }
    
    runes_data["runes"].append(new_rune)
    save_runes_data(runes_data)  # Sauvegarde après la création
    
    return True
