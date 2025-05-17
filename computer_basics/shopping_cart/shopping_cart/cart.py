import json
import random
import string

class Cart:
    def __init__(self, db_path):
        self.db_path = db_path
        self.cart = {}
        self._load_from_database()

    def _load_from_database(self):
        try:
            with open(self.db_path, 'r') as file:
                data = json.load(file)
                self.cart = data.get("items", {})
        except FileNotFoundError:
            self.cart = {}

    def _save_to_database(self):
        with open(self.db_path, 'w') as file:
            json.dump({"items": self.cart}, file, indent=4)

    def search_items(self, query):
        found = False
        for item_id, item in self.cart.items():
            if query.lower() in item['name'].lower():
                print(f"Found: {item['name']} {item['type']} ${item['price']}")
                found = True
        if not found:
            print(f"No items found for '{query}'")
        return found

    def get_total_item_count(self):
        return len(self.cart)

    def add_item_to_cart(self, item):
        item_id = ''.join(random.choices(string.ascii_uppercase, k=6))
        self.cart[item_id] = {
            "name": item.name,
            "type": item.type,
            "price": item.price
        }
        self._save_to_database()
        print(f"Added {item.name} to the cart.")

    def get_all_items(self, verbose=False):
        for item_id, item in self.cart.items():
            if verbose:
                print(item_id, item)
        return self.cart

    def remove_item_from_cart_by_query(self, query):
        for item_id, item in list(self.cart.items()):
            if query.lower() in item['name'].lower() or query.lower() in item['type'].lower():
                del self.cart[item_id]
                print(f"Removed one item matching '{query}'")
                break
        else:
            print(f"No item found matching '{query}'")
        self._save_to_database()

    # ✅ NEW METHOD
    def remove_all_items_by_query(self, query):
        keys_to_remove = [item_id for item_id, item in self.cart.items()
                          if query.lower() in item['name'].lower() or query.lower() in item['type'].lower()]
        for key in keys_to_remove:
            del self.cart[key]
        self._save_to_database()
        print(f"Removed {len(keys_to_remove)} item(s) matching '{query}' from the cart.")

    def remove_item_from_cart_by_selection(self):
        self.get_all_items(verbose=True)
        item_id = input("Enter the ID of the item to remove: ")
        if item_id in self.cart:
            del self.cart[item_id]
            self._save_to_database()
            print(f"Removed item {item_id} from the cart.")
        else:
            print("Invalid item ID.")

    def get_total_price_of_items(self):
        return sum(item['price'] for item in self.cart.values())

