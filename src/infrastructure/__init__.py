# Importar repositorios principales y modelos de ML
#from .repositories.file_book_repository import FileBookRepository
from .ml.ocr_model import OCRModel
from .ml.speech_recognition_model import SpeechRecognitionModel

__all__ = ["OCRModel", "SpeechRecognitionModel"]