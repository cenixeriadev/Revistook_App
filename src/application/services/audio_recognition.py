from pathlib import Path
import logging
from ...infrastructure.ml.speech_recognition_model import SpeechRecognitionModel
from ...domain.entities.book import Book


class AudioRecognitionService:
    def __init__(self):
        self.speech_recognizer = SpeechRecognitionModel()
        self.logger = logging.getLogger(__name__)

    async def process_audio(self, audio_path: Path | str) -> str:
        """
        Procesa un archivo de audio y lo convierte a texto
        """
        try:
            text = self.speech_recognizer.transcribe_audio(audio_path)
            return text
        except Exception as e:
            self.logger.error(f"Error processing audio {audio_path}: {str(e)}")
            raise

    async def process_book_audio(self, book: Book) -> Book:
        """
        Procesa todos los archivos de audio de un libro y actualiza su contenido
        """
        try:
            full_text = []
            for audio_file in book.audio_paths:
                text = await self.process_audio(audio_file)
                full_text.append(text)

            book.content = "\n\n".join(full_text)
            return book
        except Exception as e:
            self.logger.error(f"Error processing book audio files: {str(e)}")
            raise