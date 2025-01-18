# Importar todos los servicios
from .book_downloader import BookDownloaderService
from .text_recognition import TextRecognitionService
from .audio_recognition import AudioRecognitionService

__all__ = ["BookDownloaderService", "TextRecognitionService", "AudioRecognitionService"]