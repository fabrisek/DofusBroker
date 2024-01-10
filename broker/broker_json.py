import json
from datetime import datetime

def element_exists(elements, element_id):
    return any(element["id"] == element_id for element in elements)

def get_element_info(element_id):
    with open("data/coef_data.json", 'r') as file:
        data = json.load(file)
        elements = data.get("elements", [])

        for element in elements:
            if element["id"] == element_id:
                return element["coefficient"], element["last_update"]

        return None, None

def update_coefficient(element_id, new_coefficient):
    
    with open("data/coef_data.json", 'r') as file:
        data = json.load(file)
        elements = data.get("elements", [])

    element_found = False
    for element in elements:
        if element["id"] == element_id:
            element["coefficient"] = new_coefficient
            element["last_update"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            element_found = True

    if not element_found:
        # L'élément avec l'ID spécifié n'a pas été trouvé, créons un nouvel élément
        new_element = {
            "id": element_id,
            "coefficient": new_coefficient,
            "last_update": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        elements.append(new_element)
        print(f"Nouvel élément avec l'ID {element_id} ajouté.")

    with open("data/coef_data.json", 'w') as file:
        json.dump(data, file, indent=2)
        print(f"Coefficient pour l'élément avec ID {element_id} mis à jour ou ajouté.")

