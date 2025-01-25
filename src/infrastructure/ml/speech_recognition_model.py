import speech_recognition as sr
from pathlib import Path
import logging


class SpeechRecognitionModel:
    def __init__(self):
        """Initialize speech recognition model"""
        self.recognizer = sr.Recognizer()
        self.logger = logging.getLogger(__name__)

    def transcribe_audio(self, audio_path: str | Path) -> str:
        """
        Transcribe audio file to text

        Args:
            audio_path: Path to the audio file

        Returns:
            str: Transcribed text from the audio

        Raises:
            FileNotFoundError: If audio file doesn't exist
            Exception: For other processing errors
        """
        try:
            # Convertir a Path si es string
            audio_path = Path(audio_path) if isinstance(audio_path, str) else audio_path

            if not audio_path.exists():
                raise FileNotFoundError(f"No se encontró el archivo de audio: {audio_path}")

            # Cargar y procesar el audio
            with sr.AudioFile(str(audio_path)) as source:
                # Ajustar por ruido ambiental
                self.recognizer.adjust_for_ambient_noise(source)

                # Capturar audio
                audio = self.recognizer.record(source)

                # Realizar reconocimiento usando Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language='es-ES')
                return text.strip()

        except sr.UnknownValueError:
            self.logger.warning(f"No se pudo entender el audio en {audio_path}")
            return ""
        except sr.RequestError as e:
            self.logger.error(f"Error en el servicio de reconocimiento: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error procesando audio {audio_path}: {str(e)}")
            raise