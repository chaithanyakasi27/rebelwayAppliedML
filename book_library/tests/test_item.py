from book_library.item import Item

def test_book_price() -> None:
    book = Item("The Catcher in the Rye", "Fiction", 18.99)
    assert book.price >= 0.0 and book.price == 18.99

def test_book_name() -> None:
    book = Item("1984", "Dystopian", 14.50)
    assert len(book.name) > 0

