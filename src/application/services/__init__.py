# Importar todos los servicios
from .book_downloaderis import BookDownloader
from .audio_recognition import AudioRecognitionService
from .compare_images import CompareImagesService
__all__ = ["BookDownloader", "AudioRecognitionService" , "CompareImagesService"]