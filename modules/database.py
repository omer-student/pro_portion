import os
import json

DATA_FILE = "recipes.json"



def load_database():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            
            # Auto-Migration logic: safely converts old files if they exist
            modified = False
            for recipe_name, recipe_data in data.items():
                for ingredient in recipe_data.get("ingredients", []):
                    if "amount" in ingredient and "unit" in ingredient:
                        amount = ingredient.pop("amount")
                        unit = ingredient.pop("unit")
                        ingredient["amount_str"] = f"{amount:g}{unit}"
                        modified = True
            if modified:
                save_database(data)
            return data
        except Exception:
            return DEFAULT_RECIPES
    else:
        save_database(DEFAULT_RECIPES)
        return DEFAULT_RECIPES

def save_database(catalog_data):
    with open(DATA_FILE, "w") as f:
        json.dump(catalog_data, f, indent=4)