# src/domain/entities/book.py
class Book:
    def __init__(self, title: str, author: str, url: str):
        self.title = title
        self.author = author
        self.url = url

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, url={self.url})"

