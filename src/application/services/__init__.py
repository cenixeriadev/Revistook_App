# Importar todos los servicios
from .book_downloaderis import BookDownloader
from .text_recognition import TextRecognitionService
from .audio_recognition import AudioRecognitionService
from .compare_images import CompareImagesService
__all__ = ["BookDownloader", "TextRecognitionService", "AudioRecognitionService" , "CompareImagesService"]