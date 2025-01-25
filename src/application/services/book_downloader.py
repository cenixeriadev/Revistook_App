# src/application/services/book_downloader.py
import requests
from src.domain.entities.book import Book

class BookDownloader:
    @staticmethod
    def download_book(book: Book, download_path: str) -> str:
        try:
            response = requests.get(book.url, stream=True)
            if response.status_code == 200:
                file_path = f"{download_path}/{book.title}.pdf"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return file_path
            else:
                raise Exception(f"Failed to download book: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
            return None
