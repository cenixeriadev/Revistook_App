# src/domain/entities/book.py
from dataclasses import dataclass

@dataclass
class Book:
    id: str
    title: str
    author: str
    url: str
    cover_url: str  # Nuevo campo para la imagen
    file_format: str 

