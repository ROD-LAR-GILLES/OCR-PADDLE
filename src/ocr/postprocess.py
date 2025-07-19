import re
import pandas as pd
from typing import List, Dict, Any, Optional

class TextStructureAnalyzer:
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el analizador de estructura de texto.
        
        Args:
            config: Diccionario con configuración personalizada para la detección
        """
        self.config = config or {
            'min_title_length': 3,
            'max_title_length': 100,
            'title_markers': ['capítulo', 'sección', 'parte'],
            'min_size_ratio': 1.2  # Ratio mínimo de tamaño para considerar un título
        }
    
    def detect_title(self, text_block: Dict[str, Any]) -> bool:
        """
        Detecta si un bloque de texto es un título basado en sus características.
        
        Args:
            text_block: Diccionario con información del bloque de texto incluyendo
                       tamaño, posición, formato, etc.
        
        Returns:
            bool: True si es un título, False en caso contrario
        """
        # Verificar longitud del texto
        text = text_block.get('text', '')
        if not (self.config['min_title_length'] <= len(text) <= self.config['max_title_length']):
            return False
            
        # Verificar características de formato
        is_bold = text_block.get('is_bold', False)
        is_centered = text_block.get('is_centered', False)
        font_size = text_block.get('font_size', 0)
        base_font_size = text_block.get('base_font_size', font_size)
        
        # Calcular score basado en características
        score = 0
        if is_bold:
            score += 2
        if is_centered:
            score += 1
        if font_size / base_font_size >= self.config['min_size_ratio']:
            score += 2
            
        # Verificar palabras clave de título
        lower_text = text.lower()
        if any(marker in lower_text for marker in self.config['title_markers']):
            score += 1
            
        return score >= 3
    
    def get_hierarchy_level(self, text_block: Dict[str, Any]) -> int:
        """
        Determina el nivel jerárquico del título (1 para título principal, 2 para subtítulo, etc.)
        
        Args:
            text_block: Diccionario con información del bloque de texto
            
        Returns:
            int: Nivel jerárquico del título
        """
        font_size = text_block.get('font_size', 0)
        base_font_size = text_block.get('base_font_size', font_size)
        
        if font_size / base_font_size >= 1.5:
            return 1
        elif font_size / base_font_size >= 1.2:
            return 2
        return 3

def process_document_structure(text_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Procesa la estructura del documento detectando títulos y su jerarquía.
    
    Args:
        text_blocks: Lista de bloques de texto con sus características
        
    Returns:
        Lista de bloques de texto con información de estructura añadida
    """
    analyzer = TextStructureAnalyzer()
    structured_blocks = []
    
    for block in text_blocks:
        if analyzer.detect_title(block):
            block['is_title'] = True
            block['hierarchy_level'] = analyzer.get_hierarchy_level(block)
        else:
            block['is_title'] = False
            block['hierarchy_level'] = 0
        
        structured_blocks.append(block)
    
    return structured_blocks

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
