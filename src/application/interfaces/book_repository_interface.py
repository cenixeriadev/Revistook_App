from abc import ABC, abstractmethod
from src.domain.entities.book import Book

class BookRepositoryInterface(ABC):
    """
    Interfaz para definir los métodos que cualquier repositorio de libros debe implementar.
    """

    @abstractmethod
    def get_all_books(self) -> list[Book]:
        """
        Devuelve una lista con todos los libros almacenados.

        Returns:
            list[Book]: Lista de objetos de tipo Book.
        """
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        """
        Obtiene un libro por su ID.

        Args:
            book_id (int): El ID del libro que se quiere obtener.

        Returns:
            Book: Objeto de tipo Book correspondiente al ID.
        """
        pass

    @abstractmethod
    def save_book(self, book: Book) -> None:
        """
        Guarda un libro en el repositorio.

        Args:
            book (Book): El libro que se desea guardar.
        """
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> None:
        """
        Elimina un libro del repositorio por su ID.

        Args:
            book_id (int): El ID del libro que se desea eliminar.
        """
        pass