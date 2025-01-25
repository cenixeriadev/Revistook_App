from pathlib import Path
import logging
from ...infrastructure.ml.ocr_model import OCRModel
from ...domain.entities.book import Book


class TextRecognitionService:
    def __init__(self):
        self.ocr = OCRModel()
        self.logger = logging.getLogger(__name__)

    async def process_image(self, image_path: Path | str) -> str:
        """
        Procesa una imagen y extrae el texto usando OCR
        """
        try:
            text = self.ocr.extract_text_from_image(image_path)
            return text
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    async def process_book_images(self, book: Book) -> Book:
        """
        Procesa todas las imágenes de un libro y actualiza su contenido
        """
        try:
            full_text = []
            for page in book.image_paths:
                text = await self.process_image(page)
                full_text.append(text)

            book.content = "\n\n".join(full_text)
            return book
        except Exception as e:
            self.logger.error(f"Error processing book images: {str(e)}")
            raise
