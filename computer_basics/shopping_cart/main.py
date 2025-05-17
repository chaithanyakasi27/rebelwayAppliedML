from shopping_cart.item import Item
from shopping_cart.cart import Cart

if __name__ == "__main__":

    #the main database for the cart to pass to the class
    database = "./database.json"
    my_cart = Cart(database)

    #search for an item
    print("Searching item....")
    results = my_cart.search_items("iphone15")
    print("-------------------------")

    #get the total amount of items in the cart
    print("Total items in the current cart:")
    total_item_count = my_cart.get_total_item_count()
    print(f"Total items count: {total_item_count}")

    print("--------------------------")

    #Create an item object so it can be added to the cart
    print("Adding items to the cart:...")
    print("--------------------------")
    Nokia = Item("Nokia","Moblie", 550)
    my_cart.add_item_to_cart(Nokia)
    Oppo = Item("Oppo", "Moblie", 450)
    my_cart.add_item_to_cart(Oppo)

    #get all the items in the cart
    print("---------------------------")
    print("Getting all the items in the cart:")
    print("---------------------------")
    my_cart.get_all_items(verbose=1)

    print("---------------------------")

    #remove all items by name or type
    print("Removing all instance of an item:")
    print("---------------------------")
    my_cart.remove_all_items_by_query("Nokia")
    print("---------------------------")
    print("\n")
    #remove a selected item
    print("Removing a specific item by selection:")
    print("---------------------------")
    my_cart.remove_item_from_cart_by_selection()
    print("---------------------------")

    #show final cart contens
    print("Final items in the cart:")
    print("---------------------------")
    my_cart.get_all_items(verbose=1)

    #show final total price
    print("---------------------------")
    print("Final total price for all the item in the cart:")
    total_price = my_cart.get_total_price_of_items()
    print(f"${total_price}")
