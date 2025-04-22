# Importar servicios relevantes
from .services.book_downloaderis import BookDownloader
from .services.audio_recognition import AudioRecognitionService
from .services.compare_images import CompareImagesService

__all__ = ["BookDownloader", "AudioRecognitionService" , "CompareImagesService"]