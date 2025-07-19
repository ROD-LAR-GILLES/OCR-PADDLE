import cv2
import numpy as np
from paddleocr import PaddleOCR
import pandas as pd

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

def process_table(image):
    """
    Detecta y procesa tablas en una imagen usando PaddleOCR.
    
    Args:
        image: Imagen en formato numpy array
        
    Returns:
        Lista de DataFrames de pandas con las tablas detectadas
    """
    # Inicializar PaddleOCR con soporte para detección de estructura de tablas
    table_engine = PaddleOCR(use_angle_cls=True, lang='es', 
                            table=True, show_log=False)
    
    # Detectar tablas en la imagen
    result = table_engine.ocr(image, cls=True, table=True)
    
    tables = []
    if result:
        for table_result in result:
            if isinstance(table_result, list) and len(table_result) > 0:
                # Convertir la estructura de la tabla a un DataFrame
                try:
                    # Extraer texto y coordenadas
                    table_data = []
                    for row in table_result:
                        table_row = []
                        for cell in row:
                            if isinstance(cell, list) and len(cell) >= 2:
                                text = cell[1][0]  # Obtener el texto
                                table_row.append(text)
                        if table_row:
                            table_data.append(table_row)
                    
                    if table_data:
                        # Crear DataFrame
                        df = pd.DataFrame(table_data)
                        # Usar la primera fila como encabezados si parece apropiado
                        if df.shape[0] > 1:
                            df.columns = df.iloc[0]
                            df = df.iloc[1:]
                        tables.append(df)
                except Exception as e:
                    print(f"Error procesando tabla: {str(e)}")
                    continue
    
    return tables
