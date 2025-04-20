from pathlib import Path
import logging
from ...infrastructure.ml.feature_matching_model import FeatureMatchingModel
from ...domain.entities.book import Book

class CompareImagesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def compare_images(self, image_path: Path | str, book: Book) -> bool:
        """
        Compara dos imágenes y devuelve True si son similares
        """
        try:
            feature_matching_model = FeatureMatchingModel(image_path, book.cover_url)
            result = feature_matching_model.compare_images()
            return result
        except Exception as e:
            self.logger.error(f"Error comparing images: {str(e)}")
            raise
    