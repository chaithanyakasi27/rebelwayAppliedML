import pytest
from shopping_cart.cart import Cart
from shopping_cart.item import Item

@pytest.fixture
def cart():
    database = "./tests/test_database.json"
    # Clear the test DB before each test for isolation
    with open(database, "w") as f:
        f.write('{"items":{}}')
    return Cart(database)

def test_total_price_of_cart(cart):
    item1 = Item("Audi", "car", 2.0)
    item2 = Item("BMW", "car", 2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    # Method name matches cart.py
    assert cart.get_total_price_of_items() == 4.0

def test_empty_cart(cart):
    item = Item("a", "b", 1.2)
    cart.add_item_to_cart(item)
    # Use remove_all_items_by_query("") to clear cart
    cart.remove_all_items_by_query("")
    assert len(cart.get_all_items()) == 0

def test_search_item(cart):
    item = Item("tomato", "vegetable", 0.2)
    cart.add_item_to_cart(item)
    # search_items returns bool, so assert that it is True when found
    assert cart.search_items("tomato") is True

def test_get_all_items(cart):
    item1 = Item("Audi", "car", 2.0)
    item2 = Item("BMW", "car", 2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    retrieved_items = cart.get_all_items()
    expected_names = {item1.name, item2.name}
    actual_names = {item["name"] for item in retrieved_items.values()}
    assert expected_names == actual_names

def test_get_total_item_count(cart):
    item1 = Item("Audi", "car", 2.0)
    item2 = Item("BMW", "car", 2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    assert cart.get_total_item_count() == 2

