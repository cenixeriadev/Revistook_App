from pathlib import Path
import pytesseract
from PIL import Image
import logging


class OCRModel:
    def __init__(self):
        """Initialize OCR model using Tesseract"""
        self.logger = logging.getLogger(__name__)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

        # Verificar que tesseract está instalado
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            self.logger.error("Tesseract no está instalado o no se encuentra en el PATH")
            raise RuntimeError("Tesseract debe estar instalado para usar el OCR")

    def extract_text_from_image(self, image_path: str | Path) -> str:
        """
        Extract text from an image using OCR

        Args:
            image_path: Path to the image file

        Returns:
            str: Extracted text from the image

        Raises:
            FileNotFoundError: If image file doesn't exist
            Exception: For other processing errors
        """
        try:
            # Convertir a Path si es string
            image_path = Path(image_path) if isinstance(image_path, str) else image_path

            if not image_path.exists():
                raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

            # Abrir y procesar la imagen
            with Image.open(image_path) as img:
                # Convertir a RGB si es necesario
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Extraer texto
                text = pytesseract.image_to_string(img)
                return text.strip()

        except Exception as e:
            self.logger.error(f"Error procesando imagen {image_path}: {str(e)}")
            raise