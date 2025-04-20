import cv2
from pathlib import Path
import numpy as np
import requests
from urllib.parse import urlparse
import logging
class FeatureMatchingModel:
    def __init__(self, image_path, image_url):
        self.image_path = image_path
        self.image_url = image_url
        self.logger = logging.getLogger(__name__)
    
    
    def download_image(self , url : str) -> np.ndarray:
    # Descarga la imagen desde la URL
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            self.logger.error(f"Error al descargar la imagen: {response.status_code}")
            raise ValueError("No se pudo descargar la imagen")
        
        # Convierte los bytes de la imagen a un array de OpenCV
        image_bytes = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        return image
    
    def load_images(self):
        # Load images in grayscale
        image_url = self.download_image(self.image_url)
        img1 = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.cvtColor(image_url, cv2.COLOR_BGR2GRAY)
        return img1, img2

    def detect_and_compute(self, img : np.ndarray):
        # Initialize ORB detector
        orb = cv2.ORB_create()
        # Detect keypoints and compute descriptors
        keypoints, descriptors = orb.detectAndCompute(img, None)
        return keypoints, descriptors

    def match_features(self, des1, des2):
        # Match descriptors using Brute-Force matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)
        return matches

    def compare_images(self , min_matches=100)->bool:
        img1, img2 = self.load_images()
        kp1, des1 = self.detect_and_compute(img1)
        kp2, des2 = self.detect_and_compute(img2)

        # Si no se detectaron descriptores, abortar
        if des1 is None or des2 is None:
            self.logger.info("No se detectaron descriptores en una de las imágenes.")
            return False

        matches = self.match_features(des1, des2)

        
        self.logger.info(f"Número de matches encontrados: {len(matches)}")
        
        match_ratio = len(matches) / max(len(kp1), len(kp2)) if max(len(kp1), len(kp2)) > 0 else 0
        
        self.logger.info(f"Match ratio: {match_ratio:.2f}")
        
        return len(matches) > min_matches and match_ratio > 0.3
    #TODO: Tipar correctamente los outputs and inputs de las funciones
    
    