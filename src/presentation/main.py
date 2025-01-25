import flet as ft
from src.presentation.views.main_view import BookDownloaderApp

def main():
    app = BookDownloaderApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()