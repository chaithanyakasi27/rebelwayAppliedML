import pytest
from book_library.cart import Cart
from book_library.item import Item

@pytest.fixture
def cart():
    database = "./tests/test_database.json"
    # Clear the test DB before each test for isolation
    with open(database, "w") as f:
        f.write('{"items":{}}')
    return Cart(database)

def test_total_price_of_cart(cart):
    book1 = Item("Harry Potter and the Chamber of Secrets", "Fantasy", 15.0)
    book2 = Item("The Hobbit", "Fantasy", 20.0)
    cart.add_item_to_cart(book1)
    cart.add_item_to_cart(book2)
    assert cart.get_total_price_of_items() == 35.0

def test_empty_cart(cart):
    book = Item("1984", "Dystopian", 12.5)
    cart.add_item_to_cart(book)
    cart.remove_all_items_by_query("")
    assert len(cart.get_all_items()) == 0

def test_search_item(cart):
    book = Item("Pride and Prejudice", "Classic", 10.0)
    cart.add_item_to_cart(book)
    assert cart.search_items("Pride") is True

def test_get_all_items(cart):
    book1 = Item("Moby Dick", "Novel", 13.0)
    book2 = Item("War and Peace", "Historical", 18.0)
    cart.add_item_to_cart(book1)
    cart.add_item_to_cart(book2)
    retrieved_items = cart.get_all_items()
    expected_names = {book1.name, book2.name}
    actual_names = {item["name"] for item in retrieved_items.values()}
    assert expected_names == actual_names

def test_get_total_item_count(cart):
    book1 = Item("The Catcher in the Rye", "Classic", 11.0)
    book2 = Item("The Grapes of Wrath", "Novel", 14.0)
    cart.add_item_to_cart(book1)
    cart.add_item_to_cart(book2)
    assert cart.get_total_item_count() == 2

