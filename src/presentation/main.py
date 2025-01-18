import flet as ft
from application.services.book_downloader import BookDownloader
from application.services.text_recognition import TextRecognition
from application.services.audio_recognition import AudioRecognition


class BookDownloaderApp:
    def __init__(self):
        self.book_downloader = BookDownloader()
        self.text_recognition = TextRecognition()
        self.audio_recognition = AudioRecognition()

    def main(self, page: ft.Page):
        # Configuración de la página
        page.title = "Book Downloader"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        page.window_width = 1000
        page.window_height = 800

        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar libro",
            width=400,
            prefix_icon=ft.icons.SEARCH,
        )

        # Botones de acción
        search_button = ft.ElevatedButton(
            "Buscar",
            icon=ft.icons.SEARCH,
            on_click=self.search_book
        )

        camera_button = ft.ElevatedButton(
            "Escanear texto con cámara",
            icon=ft.icons.CAMERA_ALT,
            on_click=self.scan_text
        )

        audio_button = ft.ElevatedButton(
            "Reconocer audio",
            icon=ft.icons.MIC,
            on_click=self.recognize_audio
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

        # Estado de la descarga
        self.status_text = ft.Text(
            size=16,
            color=ft.colors.GREY_500
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
                                    on_click=lambda e: self.download_book(book)
                                )
                            ]
                        )
                    ]
                ),
                padding=10
            )
        )

    async def scan_text(self, e):
        # Implementar la lógica de escaneo de texto con la cámara
        self.status_text.value = "Escaneando texto..."
        self.page.update()

        try:
            text = await self.text_recognition.scan()
            self.search_field.value = text
            self.page.update()
        except Exception as ex:
            self.status_text.value = f"Error al escanear: {str(ex)}"
            self.page.update()

    async def recognize_audio(self, e):
        # Implementar la lógica de reconocimiento de audio
        self.status_text.value = "Escuchando..."
        self.page.update()

        try:
            text = await self.audio_recognition.recognize()
            self.search_field.value = text
            self.page.update()
        except Exception as ex:
            self.status_text.value = f"Error al reconocer audio: {str(ex)}"
            self.page.update()

    async def download_book(self, book):
        self.progress_bar.visible = True
        self.status_text.value = f"Descargando {book.title}..."
        self.page.update()

        try:
            await self.book_downloader.download(book)
            self.status_text.value = "Descarga completada"
        except Exception as ex:
            self.status_text.value = f"Error en la descarga: {str(ex)}"
        finally:
            self.progress_bar.visible = False
            self.page.update()


def main():
    app = BookDownloaderApp()
    ft.app(target=app.main)


if __name__ == "__main__":
    main()