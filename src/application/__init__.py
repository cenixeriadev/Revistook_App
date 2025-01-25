# Importar servicios relevantes
from .services.book_downloader import BookDownloader
from .services.text_recognition import TextRecognitionService
from .services.audio_recognition import AudioRecognitionService

__all__ = ["BookDownloader", "TextRecognitionService", "AudioRecognitionService"]