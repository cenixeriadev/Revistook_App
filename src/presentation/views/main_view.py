# src/presentation/views/main_view.py
import shutil

import flet as ft
from pathlib import Path
import os
from datetime import datetime
import asyncio
from src.application.services.book_downloader import BookDownloader
from src.application.services.text_recognition import TextRecognitionService
from src.application.services.audio_recognition import AudioRecognitionService
from src.domain.entities.download_status import DownloadStatus, DownloadState


class BookDownloaderApp:
    def __init__(self):
        self.book_downloader = BookDownloader()
        self.text_recognition = TextRecognitionService()
        self.audio_recognition = AudioRecognitionService()
        self.page = None
        self.download_tasks = {}
        self.setup_directories()

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

        # Configuración de la página
        page.title = "Book Downloader"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.window_width = 1000
        page.window_height = 800

        # Configurar File Picker para imágenes
        self.image_picker = ft.FilePicker(
            on_result=self.handle_image_picked
        )

        # Configurar File Picker para audio
        self.audio_picker = ft.FilePicker(
            on_result=self.handle_audio_picked
        )

        # Agregar file pickers a la página
        page.overlay.extend([self.image_picker, self.audio_picker])

        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar libro",
            width=400,
            prefix_icon=ft.icons.SEARCH,
            multiline=True,
            min_lines=3,
            max_lines=5
        )

        # Botones de acción
        search_button = ft.ElevatedButton(
            "Buscar",
            icon=ft.icons.SEARCH,
            on_click=self.search_book
        )

        # Botón para capturar imagen
        camera_button = ft.ElevatedButton(
            "Capturar imagen",
            icon=ft.icons.CAMERA_ALT,
            on_click=lambda _: self.image_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        )

        # Botón para grabar audio
        audio_button = ft.ElevatedButton(
            "Seleccionar audio",
            icon=ft.icons.MIC,
            on_click=lambda _: self.audio_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=['wav', 'mp3']
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
                ft.Text("Book Downloader", size=32, weight=ft.FontWeight.BOLD),
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
                        audio_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                self.preview,
                self.progress_bar,
                self.status_text,
                ft.Container(
                    content=self.results_list,
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=10,
                    padding=10
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        page.add(main_content)

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

                # Mostrar vista previa
                self.preview.src = str(image_path)
                self.preview.visible = True

                # Procesar imagen con OCR
                self.status_text.value = "Procesando imagen..."
                self.page.update()

                text = await self.text_recognition.process_image(str(image_path))

                # Agregar el texto al campo de búsqueda
                current_text = self.search_field.value or ""
                self.search_field.value = current_text + "\n" + text if current_text else text

                self.status_text.value = "Imagen procesada correctamente"

        except Exception as ex:
            self.status_text.value = f"Error procesando imagen: {str(ex)}"
        finally:
            self.page.update()
    def toggle_recording(self, e):
        """Inicia o detiene la grabación de audio"""
        if self.audio_recorder.recording:
            self.audio_recorder.stop()
            e.control.icon = ft.icons.MIC
            e.control.text = "Grabar audio"
            self.status_text.value = "Grabación finalizada"
        else:
            self.audio_recorder.record()
            e.control.icon = ft.icons.STOP
            e.control.text = "Detener grabación"
            self.status_text.value = "Grabando..."
        self.page.update()

    async def handle_audio_picked(self, e: ft.FilePickerResultEvent):
        """Maneja la selección de audio"""
        try:
            if e.files and len(e.files) > 0:
                file_path = e.files[0].path

                # Generar nombre único para el audio
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_name = f"book_audio_{timestamp}{Path(file_path).suffix}"
                audio_path = Path(self.audio_dir) / audio_name

                # Copiar audio al directorio de audios
                shutil.copy2(file_path, audio_path)

                # Procesar audio
                self.status_text.value = "Procesando audio..."
                self.page.update()

                text = await self.audio_recognition.process_audio(str(audio_path))

                # Agregar el texto al campo de búsqueda
                current_text = self.search_field.value or ""
                self.search_field.value = current_text + "\n" + text if current_text else text

                self.status_text.value = "Audio procesado correctamente"

        except Exception as ex:
            self.status_text.value = f"Error procesando audio: {str(ex)}"
        finally:
            self.page.update()

    def create_book_card(self, book):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(book.title, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(book.author),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Descargar",
                                    icon=ft.icons.DOWNLOAD,
                                    on_click=lambda e: self.start_download(book)
                                )
                            ]
                        ),
                        ft.ProgressBar(
                            width=300,
                            visible=False,
                            value=0,
                            bgcolor=ft.colors.GREY_200,
                            color=ft.colors.BLUE,
                        )
                    ]
                ),
                padding=10
            )
        )


    async def search_book(self, e):
        search_term = self.search_field.value
        if not search_term:
            return

        self.progress_bar.visible = True
        self.status_text.value = "Buscando libros..."
        self.page.update()

        try:
            results = await self.book_downloader.search(search_term)
            self.results_list.controls.clear()

            for book in results:
                self.results_list.controls.append(
                    self.create_book_card(book)
                )
        except Exception as ex:
            self.status_text.value = f"Error: {str(ex)}"
        finally:
            self.progress_bar.visible = False
            self.page.update()

    def start_download(self, book):
        # Crear status para esta descarga
        status = DownloadStatus(
            id=str(book.id),
            state=DownloadState.PENDING
        )

        # Iniciar descarga en segundo plano
        task = asyncio.create_task(self.download_book(book, status))
        self.download_tasks[book.id] = (task, status)

    async def download_book(self, book, status):
        progress_bar = self.find_book_progress_bar(book)
        if not progress_bar:
            return

        progress_bar.visible = True
        self.page.update()

        try:
            status.state = DownloadState.DOWNLOADING

            # Simular progreso de descarga
            for i in range(0, 101, 10):
                status.update_progress(i)
                progress_bar.value = i / 100
                await asyncio.sleep(0.5)  # Simular descarga
                self.page.update()

            await self.book_downloader.download(
                book,
                Path(self.directory_picker.value)
            )

            status.complete()
            progress_bar.value = 1
            self.status_text.value = f"{book.title} descargado correctamente"

        except Exception as ex:
            status.fail(str(ex))
            self.status_text.value = f"Error en la descarga: {str(ex)}"
        finally:
            self.page.update()

    def find_book_progress_bar(self, book):
        # Buscar la barra de progreso en el card del libro
        for control in self.results_list.controls:
            if isinstance(control, ft.Card):
                column = control.content.content
                for sub_control in column.controls:
                    if isinstance(sub_control, ft.ProgressBar):
                        return sub_control
        return None



