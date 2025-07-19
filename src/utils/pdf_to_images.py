from pdf2image import convert_from_path
import numpy as np

def convert_pdf_to_images(pdf_path):
    """
    Convierte un archivo PDF a una lista de imágenes.
    
    Args:
        pdf_path: Ruta al archivo PDF
        
    Returns:
        Lista de imágenes en formato numpy array
    """
    # Convertir PDF a imágenes
    images = convert_from_path(pdf_path)
    
    # Convertir las imágenes a formato numpy array
    return [np.array(img) for img in images]
