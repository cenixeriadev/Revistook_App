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
from typing import Optional, Callable

@DeprecationWarning
class BookDownloader:
    def __init__(self):
        self.driver = None
        self.base_url = "https://libgen.li/"
        
    async def initialize_driver(self):
        """Inicializa el driver de Selenium en un hilo separado"""
        loop = asyncio.get_event_loop()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Ejecución en segundo plano
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

            WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[@for="covers"]'))
            ).click()
            
            # Buscar elementos y escribir
            search_form = await self.find_element(By.XPATH, '/html/body/form/div[1]/input')
            search_form.send_keys(query)

            # Hacer clic en botón de búsqueda
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[1]/div[1]/button'))
            )
            search_button.click()

            # Ordenar por año
            BtnYear = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tablelibgen"]/thead/tr/th[5]/nobr/a'))
            )
            BtnYear.click()
            BtnYear = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tablelibgen"]/thead/tr/th[5]/nobr/a'))
            )
            BtnYear.click() # ponemos primero los libros más nuevos
            
            # Obtener resultados (adaptar según estructura real de la página)
            books = []
            WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tablelibgen"]/tbody/tr'))
            )
            rows = await self.find_elements(By.XPATH, '//*[@id="tablelibgen"]/tbody/tr')
            

            for i, row in enumerate(rows[1:10]):
                cells = row.find_elements(By.TAG_NAME, 'td')
                try:
                    img_element = cells[0].find_element(By.TAG_NAME, 'img')
                
                    
                    cover_url = img_element.get_attribute('src').replace('_small' , '')
                    
                    if cover_url=='':
                        cover_url = "https://e7.pngegg.com/pngimages/829/733/png-clipart-logo-brand-product-trademark-font-not-found-logo-brand.png"
                    if not cover_url.startswith('http' or 'https'):
                        cover_url = f"{self.base_url.rstrip('/')}{cover_url}"
    
                    
                except:
                    cover_url = ""
                
                book = Book(
                    id=str(i),
                    title=cells[1].find_elements(By.TAG_NAME, 'a')[0].text,
                    author=cells[2].text,
                    url=cells[9].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'),
                    cover_url=cover_url
                )
                books.append(book)
            
            return books

        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []

    async def download(
        self, 
        book: Book, 
        download_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Optional[str]:
        try:
            await self.get_download_url(book)
            return await self.download_file(
                book.url, 
                download_path, 
                book.title,
                progress_callback
            )
        except Exception as e:
            print(f"Error final en descarga: {str(e)}")
            return None
    async def get_download_url(self, book: Book):
        """Obtiene la URL directa de descarga"""
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.driver.get(book.url)
        )
        
        download_link = await self.find_element(By.XPATH, '/html/body/table/tbody/tr[1]/td[2]/a')
        book.url = download_link.get_attribute('href')

    async def download_file(
        self, 
        url: str, 
        path: str, 
        filename: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    )-> str:
        """Descarga asíncrona con seguimiento de progreso"""
        import aiohttp
        from aiohttp import ClientSession
        
        # Sanitizar nombre de archivo
        def sanitize(name):
            return "".join(c for c in name if c.isalnum() or c in " .-_")
        
        sanitized_name = sanitize(filename)
        file_path = os.path.join(path, f"{sanitized_name}.pdf")
        
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    
                    with open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Actualizar progreso
                            if progress_callback:
                                # Ejecutar en el event loop principal
                                await progress_callback(downloaded, total_size)
                    
                    return file_path
                    
        except Exception as e:
            print(f"Error en descarga: {str(e)}")
            if os.path.exists(file_path):
                os.remove(file_path)
            return None 

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