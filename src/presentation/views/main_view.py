# src/presentation/views/main_view.py
import shutil

import flet as ft
from pathlib import Path
import os
from datetime import datetime
import asyncio
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from datetime import datetime
from src.application.services.book_downloaderis import BookDownloader
from src.application.services.compare_images import CompareImagesService
from src.application.services.audio_recognition import AudioRecognitionService
from src.domain.entities.download_status import DownloadStatus, DownloadState
import logging


class BookDownloaderApp:
    def __init__(self):
        self.book_downloader = BookDownloader()
        self.audio_recognition = AudioRecognitionService()
        self.compare_images = CompareImagesService()
        self.page = None
        self.download_tasks = {}
        self.setup_directories()
        self.directory_picker = ft.FilePicker(on_result=self.handle_directory_picked)
        self.download_dir = str(Path.home() / "Downloads")
        self.is_recording = False
        self.recording_filename = None
        self.audio_data = []

    def setup_directories(self):
        """Configura los directorios para guardar imágenes y audios"""
        # Obtener directorios estándar del usuario
        if os.name == 'nt':  # Windows
            self.pictures_dir = str(Path.home() / 'Pictures' / 'BookDownloader')
            self.audio_dir = str(Path.home() / 'Music' / 'BookDownloader')
        else:  # Linux/Mac
            self.pictures_dir = str(Path.home() / 'Pictures' / 'BookDownloader')
            self.audio_dir = str(Path.home() / 'Music' / 'BookDownloader')

        # Crear directorios si no existen
        Path(self.pictures_dir).mkdir(parents=True, exist_ok=True)
        Path(self.audio_dir).mkdir(parents=True, exist_ok=True)

    def main(self, page: ft.Page):
        self.page = page
        page.on_close = self.on_page_close
        # Configuración de la página
        page.title = "REVISTOOK"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        page.window_width = 1000
        page.window_height = 800

        # Configurar File Picker para imágenes
        self.image_picker = ft.FilePicker(
            on_result=self.handle_image_picked
        )
        self.record_button = ft.ElevatedButton(
            "Grabar audio",
            icon=ft.icons.MIC,
            on_click=self.toggle_recording
        )

        # Agregar componentes a la
        page.overlay.extend([self.image_picker, self.directory_picker])


        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar libro",
            width=300,
            height= 60,
            prefix_icon=ft.icons.SEARCH,
            multiline=True,
            min_lines=1,
            max_lines=5
        )

        # Botones de acción
        search_button = ft.ElevatedButton(
            "Buscar",
            icon=ft.icons.SEARCH,
            on_click=self.search_book
        )
        directory_button = ft.ElevatedButton(
            "Seleccionar carpeta",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: self.directory_picker.get_directory_path()
        )

        # Botón para capturar imagen
        camera_button = ft.ElevatedButton(
            "Filtrar por imagen",
            icon=ft.icons.CAMERA_ALT,
            on_click=lambda _: self.image_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        )

        # Lista de resultados
        self.results_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            height=400
        )

        # Barra de progreso
        self.progress_bar = ft.ProgressBar(
            width=400,
            visible=False
        )

        # Estado de la operación
        self.status_text = ft.Text(
            size=16,
            color=ft.colors.GREY_500
        )

        # Vista previa de imagen
        self.preview = ft.Image(
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN,
            visible=False
        )

        # Contenedor principal
        main_content = ft.Column(
            controls=[
                ft.Text("📚🆓", size=32, weight=ft.FontWeight.NORMAL ),
                ft.Row(
                    controls=[
                        self.search_field,
                        search_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        camera_button,
                        self.record_button,
                        directory_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                ft.Text(f"Descargas en: {self.download_dir}", size=12, color=ft.colors.GREY_500),
                self.preview,
                self.progress_bar,
                self.status_text,
                ft.Container(
                    content=self.results_list,
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=10,
                    padding=10
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        page.add(main_content)

    def on_page_close(self):
        """Maneja el cierre de la página"""
        self.page = None    
    async def handle_image_picked(self, e: ft.FilePickerResultEvent):
        """Maneja la selección de imagen"""
        try:
            if e.files and len(e.files) > 0:
                file_path = e.files[0].path

                # Generar nombre único para la imagen
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_name = f"book_scan_{timestamp}{Path(file_path).suffix}"
                image_path = Path(self.pictures_dir) / image_name

                # Copiar imagen al directorio de imágenes
                shutil.copy2(file_path, image_path)

                print(image_path)


                self.progress_bar.visible = True
                self.status_text.value = "Filtrando libros..."
                self.page.update()
                
                self.results_list.controls.clear()
                
                self.results_list.update()
                for  book in self.current_results:
                    result = await self.compare_images.compare_images(image_path, book)
                    print(f"Comparando con {book.title}: {result}")
                    if result:
                        self.results_list.controls.append(self.create_book_card(book))
                        self.results_list.update()
                    else:
                        print(f"El libro {book.title} no coincide con la imagen.")

                
                self.status_text.value = "Imagen procesada correctamente"
                self.page.update()
        except Exception as ex:
            self.status_text.value = f"Error filtrando por  imagen: {str(ex)}"
        finally:
            self.progress_bar.visible = False
            self.page.update()
            
    def handle_directory_picked(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.download_dir = e.path
            self.status_text.value = f"Directorio de descarga: {self.download_dir}"
            self.page.update()

    def start_recording(self):
        self.is_recording = True
        self.record_button.icon = ft.icons.STOP
        self.record_button.text = "Detener grabación"
        self.status_text.value = "Grabando..."
        self.page.update()
        
        # Configuración de grabación
        self.recording_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        self.audio_data = []
        
        # Inicia grabación en segundo plano
        sd.default.samplerate = 16000
        sd.default.channels = 1
        sd.default.dtype = 'int16'
        
        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()
    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_data.append(indata.copy())
    def stop_recording(self):
        self.is_recording = False
        self.record_button.icon = ft.icons.MIC
        self.record_button.text = "Grabar audio"
        self.status_text.value = "Procesando grabación..."
        self.page.update()
        
        # Detener grabación
        self.stream.stop()
        self.stream.close()
        
        # Guardar archivo WAV
        audio_path = Path(self.audio_dir) / self.recording_filename
        audio_data = np.concatenate(self.audio_data)
        write(str(audio_path), 16000, audio_data)
        
        # Procesar audio
        asyncio.run_coroutine_threadsafe(
            self.process_recorded_audio(audio_path),
            self.page.loop
        )
    async def process_recorded_audio(self, audio_path):
        try:
            # Convertir si es necesario (en este caso ya está en WAV)
            text = await self.audio_recognition.process_audio(audio_path)
            
            # Actualizar campo de búsqueda
            current_text = self.search_field.value or ""
            self.search_field.value = f"{current_text}\n{text}" if current_text else text
            self.status_text.value = "Grabación procesada correctamente"
        except Exception as ex:
            self.status_text.value = f"Error procesando grabación: {str(ex)}"
        finally:
            self.page.update()
    def toggle_recording(self, e):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def create_book_card(self, book):
        cover_image = ft.Image(
            src=book.cover_url if book.cover_url else "https://png.pngtree.com/png-clipart/20190925/original/pngtree-no-image-vector-illustration-isolated-png-image_4979075.jpg",
            width=100,
            height=150,
            fit=ft.ImageFit.CONTAIN,
            border_radius=5
        )
        
        # Crear contenedor para el estado de la descarga
        download_status = ft.Text(
            size=12,
            color=ft.colors.CYAN_600,
            visible=False
        )
        
        progress_bar = ft.ProgressBar(
            width=200,
            visible=False,
            value=0,
            bgcolor=ft.colors.LIGHT_GREEN,
            color=ft.colors.GREEN_200,
        )
        
        download_button = ft.ElevatedButton(
            "Descargar",
            icon=ft.icons.DOWNLOAD,
            on_click=lambda e: self.start_download(e, book, progress_bar, download_button, download_status)
        )

        card = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        cover_image,
                        ft.Column(
                            controls=[
                                ft.Text(book.title, size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(book.author, size=14, color=ft.colors.GREY_600),
                                ft.Row([download_button]),
                                progress_bar,
                                download_status
                            ],
                            expand=True,
                            spacing=10
                        )
                    ],
                    spacing=15
                ),
                padding=15
            ),
            elevation=3
        )
        return card
    async def search_book(self, e):
        search_term = self.search_field.value
        if not search_term:
            return

        self.progress_bar.visible = True
        self.status_text.value = "Buscando libros..."
        self.page.update()

        try:
            self.current_results = await self.book_downloader.search(search_term)
            self.books_dict = {b.id: b for b in self.current_results}
            self.results_list.controls.clear()

            for book in self.current_results:
                self.results_list.controls.append(
                    self.create_book_card(book)
                )
        except Exception as ex:
            self.status_text.value = f"Error: {str(ex)}"
        finally:
            self.progress_bar.visible = False
            self.status_text.value = ""
            self.page.update()

    def start_download(self, e, book, progress_bar, download_button, download_status):
        """Inicia la descarga de un libro"""
        status = DownloadStatus(
            id=str(book.id),
            state=DownloadState.PENDING
        )
        # Deshabilitar el botón durante la descarga
        download_button.disabled = True
        self.page.update()
        self.page.run_task(self.download_book, book, status, progress_bar, download_button, download_status)

    # En main_view.py, actualizar el método de descarga:
    async def download_book(self, book, status, progress_bar, download_button, download_status):
        """Descarga un libro y actualiza la UI"""
        try:
            status.state = DownloadState.DOWNLOADING
            progress_bar.visible = True
            download_status.visible = True
            download_status.value = "Iniciando descarga..."
            
            self.page.update()
            
            download_path = self.download_dir
            Path(download_path).mkdir(parents=True, exist_ok=True)
            
            async def update_progress(current: int, total: int):
                if total > 0:
                    progress = current / total
                    progress_bar.value = progress
                    download_status.value = f"Descargando... {int(progress * 100)}%"
                    self.page.update()
            
            file_path = await self.book_downloader.download(
                book, 
                download_path,
                progress_callback=update_progress
            )
            
            if file_path:
                status.complete()
                download_status.value = "¡Descarga completada!"
                download_status.color = ft.colors.GREEN
            else:
                status.fail("Error en la descarga")
                download_status.value = "Error en la descarga"
                download_status.color = ft.colors.RED
                
        except Exception as ex:
            status.fail(str(ex))
            download_status.value = f"Error: {str(ex)}"
            download_status.color = ft.colors.RED
        finally:
            progress_bar.visible = False
            download_button.disabled = False
            self.page.update()
    
    async def safe_update(self):
        """Actualiza la página de forma segura"""
        if self.page and not self.page._close:
            await self.page.update_async()

    async def update_progress_ui(self, book, progress: float):
        """Actualiza la UI de forma asíncrona"""
        if not self.page or self.page._close:
            return
        
        progress_bar = self.find_book_progress_bar(book)
        if progress_bar and progress_bar in self.page.controls:
            progress_bar.value = progress
            await self.safe_update()

