# Marcar el directorio como un paquete
# Opcionalmente, importar entidades o interfaces clave
from .entities.book import Book
from .entities.download_status import DownloadStatus
from .interfaces.book_repository_interface import BookRepositoryInterface

__all__ = ["Book", "DownloadStatus", "BookRepositoryInterface"]