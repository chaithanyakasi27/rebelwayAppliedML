from book_library.item import Item
from book_library.cart import Cart

if __name__ == "__main__":

    # The database file path
    database = "./database.json"
    my_cart = Cart(database)

    # Search for an item
    print("Searching item....")
    my_cart.search_items("Harry Potter")
    print("-------------------------")

    # Get the total amount of items in the cart
    print("Total items in the current cart:")
    total_item_count = my_cart.get_total_item_count()
    print(f"Total items count: {total_item_count}")

    print("--------------------------")

    # Create Item objects and add to cart
    print("Adding items to the cart:")
    print("--------------------------")
    hp_stone = Item("Harry Potter and the Sorcerer's Stone", "Fantasy", 12.99)
    my_cart.add_item_to_cart(hp_stone)

    gatsby = Item("The Great Gatsby", "Novel", 10.50)
    my_cart.add_item_to_cart(gatsby)

    mockingbird = Item("To Kill a Mockingbird", "Classic", 9.99)
    my_cart.add_item_to_cart(mockingbird)

    print("---------------------------")
    print("Getting all the items in the cart:")
    print("---------------------------")
    my_cart.get_all_items(verbose=True)

    print("---------------------------")

    # Remove all items by name or type
    print("Removing all instance of an item:")
    print("---------------------------")
    my_cart.remove_all_items_by_query("Gatsby")
    print("---------------------------")
    print("\n")

    # Remove a specific item by selection
    print("Removing a specific item by selection:")
    print("---------------------------")
    my_cart.remove_item_from_cart_by_selection()
    print("---------------------------")

    # Show final cart contents
    print("Final items in the cart:")
    print("---------------------------")
    my_cart.get_all_items(verbose=True)

    # Show final total price
    print("---------------------------")
    print("Final total price for all the items in the cart:")
    total_price = my_cart.get_total_price_of_items()
    print(f"${total_price:.2f}")

