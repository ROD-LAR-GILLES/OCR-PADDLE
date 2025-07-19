import re
import pandas as pd
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """
    Limpia el texto eliminando caracteres no deseados y normalizando espacios.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    # Eliminar caracteres especiales y normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Normalizar puntuación
    text = re.sub(r'\.{2,}', '.', text)  # Eliminar puntos múltiples
    text = re.sub(r'\,{2,}', ',', text)  # Eliminar comas múltiples
    
    return text

def format_table(df: pd.DataFrame) -> str:
    """
    Formatea una tabla pandas como Markdown.
    
    Args:
        df: DataFrame de pandas a formatear
        
    Returns:
        Tabla formateada en Markdown
    """
    # Limpiar los nombres de las columnas
    df.columns = [clean_text(str(col)) for col in df.columns]
    
    # Limpiar los valores de la tabla
    df = df.applymap(lambda x: clean_text(str(x)) if pd.notnull(x) else '')
    
    # Convertir a Markdown con alineación centrada
    md_table = df.to_markdown(index=False, tablefmt='pipe')
    
    return md_table

def format_as_markdown(text: str, tables: List[pd.DataFrame] = None) -> str:
    """
    Formatea el texto y las tablas en Markdown.
    
    Args:
        text: Texto principal del documento
        tables: Lista de DataFrames con las tablas detectadas
        
    Returns:
        Documento formateado en Markdown
    """
    # Limpiar y formatear el texto principal
    paragraphs = text.split('\n\n')
    formatted_text = []
    
    for p in paragraphs:
        if p:
            # Limpiar el párrafo
            clean_p = clean_text(p)
            
            # Detectar si es un encabezado (por ejemplo, si está en mayúsculas)
            if p.isupper():
                formatted_text.append(f'\n## {clean_p}\n')
            else:
                formatted_text.append(clean_p)
    
    # Unir el texto principal
    main_text = '\n\n'.join(formatted_text)
    
    # Agregar las tablas si existen
    if tables:
        table_section = '\n\n## Tablas Detectadas\n\n'
        for i, table in enumerate(tables, 1):
            table_section += f'\n### Tabla {i}\n\n'
            table_section += format_table(table)
            table_section += '\n\n---\n'
        main_text += table_section
    
    # Agregar metadatos y pie de página
    markdown_doc = f"""# Documento Procesado con OCR

{main_text}

---
*Procesado con PaddleOCR*
"""
    
    return markdown_doc

def process_sections(text: str) -> Dict[str, Any]:
    """
    Procesa el texto para identificar secciones y estructuras.
    
    Args:
        text: Texto a procesar
        
    Returns:
        Diccionario con las secciones identificadas
    """
    sections = {}
    
    # Identificar encabezados
    headers = re.finditer(r'^[A-Z][A-Z\s]+[A-Z]$', text, re.MULTILINE)
    for match in headers:
        header = match.group()
        sections[header] = []
    
    # Identificar posibles listas
    list_items = re.finditer(r'^\d+\.\s+(.+)$', text, re.MULTILINE)
    if list_items:
        sections['LISTAS'] = [item.group(1) for item in list_items]
    
    return sections
