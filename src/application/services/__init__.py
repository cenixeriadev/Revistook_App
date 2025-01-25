# Importar todos los servicios
from .book_downloader import BookDownloader
from .text_recognition import TextRecognitionService
from .audio_recognition import AudioRecognitionService

__all__ = ["BookDownloader", "TextRecognitionService", "AudioRecognitionService"]