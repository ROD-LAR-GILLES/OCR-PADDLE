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
    tables = []
    try:
        # Inicializar PaddleOCR con el modelo específico para tablas
        table_engine = PaddleOCR(
            use_angle_cls=True,
            lang='es',
            table=True,
            show_log=False
        )
        
        # Detectar tablas en la imagen usando el modo específico para tablas
        result = table_engine.ocr(image, rec=True, cls=True)
        print("Resultado de detección de tabla:", result)  # Para depuración
    except Exception as e:
        print(f"Error en la detección de tablas: {str(e)}")
        return []
    if result:
        # La estructura del resultado es diferente cuando se usa el modo tabla
        for table_result in result:
            try:
                # Convertir la estructura de la tabla a un DataFrame
                table_data = []
                if isinstance(table_result, list):
                    for row in table_result:
                        row_data = []
                        if isinstance(row, list):
                            for cell in row:
                                if isinstance(cell, list) and len(cell) >= 2:
                                    text = cell[1][0]  # Texto reconocido
                                    confidence = cell[1][1]  # Confianza
                                    if confidence > 0.5:  # Solo incluir si la confianza es alta
                                        row_data.append(text)
                                    else:
                                        row_data.append('')
                            if any(row_data):  # Solo agregar filas que tengan algún contenido
                                table_data.append(row_data)
                
                if table_data:
                    # Crear DataFrame
                    df = pd.DataFrame(table_data)
                    # Usar la primera fila como encabezados si parece apropiado
                    if df.shape[0] > 1:
                        df.columns = df.iloc[0]
                        df = df.iloc[1:]
                    tables.append(df)
                    print(f"Tabla detectada con dimensiones: {df.shape}")  # Para depuración
            except Exception as e:
                print(f"Error procesando tabla: {str(e)}")
                continue
    
    return tables
