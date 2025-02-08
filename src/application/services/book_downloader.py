# src/application/services/book_downloader.py
# src/application/services/book_downloader.py
import os
import asyncio
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.domain.entities.book import Book

class BookDownloader:
    def __init__(self):
        self.driver = None
        self.base_url = "https://libgen.is/"
        
    async def initialize_driver(self):
        """Inicializa el driver de Selenium en un hilo separado"""
        loop = asyncio.get_event_loop()
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")  # Ejecución en segundo plano
        self.driver = await loop.run_in_executor(
            None, 
            lambda: webdriver.Chrome(options=chrome_options)
        )

    async def search(self, query: str) -> List[Book]:
        """Búsqueda asíncrona de libros"""
        if not self.driver:
            await self.initialize_driver()

        try:
            # Ejecutar acciones de Selenium en un executor
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.driver.get(self.base_url)
            )

            # Realizar la búsqueda
            search_form = await self.find_element(By.XPATH, '//*[@id="searchform"]')
            search_form.send_keys(query)
            search_button = await self.find_element(By.XPATH, '/html/body/table/tbody[2]/tr/td[2]/form/input[2]')
            search_button.click()

            # Obtener resultados (adaptar según estructura real de la página)
            books = []
            rows = await self.find_elements(By.XPATH, '//table[3]/tbody/tr')
            for i, row in enumerate(rows[1:6]):  # Primeros 5 resultados
                cells = row.find_elements(By.TAG_NAME, 'td')
                book = Book(
                    id=str(i),
                    title=cells[2].text,
                    author=cells[1].text,
                    url=cells[9].find_element(By.TAG_NAME, 'a').get_attribute('href')
                )
                books.append(book)
            for i, row in enumerate(rows[1:6]):
                cells = row.find_elements(By.TAG_NAME, 'td')
                try:
                    img_element = cells[0].find_element(By.TAG_NAME, 'img')
                    cover_url = img_element.get_attribute('src')
                    # Convertir a URL absoluta si es necesario
                    if not cover_url.startswith('http'):
                        cover_url = f"{self.base_url.rstrip('/')}{cover_url}"
                except:
                    cover_url = ""
                
                book = Book(
                    id=str(i),
                    title=cells[2].text,
                    author=cells[1].text,
                    url=cells[9].find_element(By.TAG_NAME, 'a').get_attribute('href'),
                    cover_url=cover_url
                )
                books.append(book)
            return books

        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []

    async def download(self, book: Book, download_path: str) -> str:
        """Descarga asíncrona del libro"""
        try:
            # Obtener URL directa del libro
            await self.get_download_url(book)
            
            # Descargar el archivo
            return await self.download_file(book.url, download_path, book.title)
            
        except Exception as e:
            print(f"Error en descarga: {e}")
            return None

    async def get_download_url(self, book: Book):
        """Obtiene la URL directa de descarga"""
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.driver.get(book.url)
        )
        
        download_link = await self.find_element(By.XPATH, '//h2/a')
        book.url = download_link.get_attribute('href')

    async def download_file(self, url: str, path: str, filename: str) -> str:
        """Descarga el archivo usando requests"""
        from requests import get
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: get(url, stream=True)
        )
        
        file_path = os.path.join(path, f"{filename}.pdf")
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return file_path

    async def close(self):
        """Cierra el driver"""
        if self.driver:
            await asyncio.get_event_loop().run_in_executor(None, self.driver.quit)

    # Helpers para ejecutar Selenium de forma asíncrona
    async def find_element(self, by, value):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
        )

    async def find_elements(self, by, value):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((by, value))
            )
        )