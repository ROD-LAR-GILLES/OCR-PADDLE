import cv2
import numpy as np
from paddleocr import PaddleOCR

def process_document(images):
    """
    Procesa una lista de imágenes usando PaddleOCR.
    
    Args:
        images: Lista de imágenes en formato numpy array
        
    Returns:
        Lista de textos extraídos de las imágenes
    """
    # Inicializar PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='es')
    results = []
    
    for img in images:
        # Realizar OCR en la imagen
        result = ocr.ocr(img, cls=True)
        
        # Extraer el texto de los resultados
        if result:
            page_text = []
            for line in result:
                if line:
                    for word_info in line:
                        if len(word_info) >= 2:  # Asegurarse de que hay texto
                            text = word_info[1][0]  # Obtener el texto
                            page_text.append(text)
            results.append(' '.join(page_text))
        else:
            results.append('')  # Página sin texto
    
    return results
