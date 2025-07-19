import os
import argparse
from pathlib import Path
from ocr.processor import process_document
from utils.pdf_to_images import convert_pdf_to_images

def save_as_markdown(text, output_path):
    """Guarda el texto en formato Markdown."""
    # Convertir el texto a formato Markdown
    md_content = f"""# Documento OCR Procesado

## Contenido del documento

{text}

---
*Procesado con PaddleOCR*
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

def process_single_file(pdf_path: str, output_dir: str):
    """Procesa un único archivo PDF."""
    if not pdf_path.endswith('.pdf'):
        print(f"Error: {pdf_path} no es un archivo PDF")
        return False
    
    print(f"Procesando {pdf_path}...")
    try:
        # Convertir PDF a imágenes
        images = convert_pdf_to_images(pdf_path)
        
        # Procesar cada imagen con OCR
        results = process_document(images)
        
        # Guardar resultados
        filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(filename)[0]
        
        # Guardar como texto plano
        txt_path = os.path.join(output_dir, f"{base_name}_ocr.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
            
        # Guardar como Markdown
        md_path = os.path.join(output_dir, f"{base_name}_ocr.md")
        save_as_markdown('\n\n'.join(results), md_path)
            
        print(f"Archivo procesado exitosamente:")
        print(f"- Texto plano: {txt_path}")
        print(f"- Markdown: {md_path}")
        return True
    except Exception as e:
        print(f"Error procesando {pdf_path}: {str(e)}")
        return False

def process_directory(input_dir: str, output_dir: str):
    """Procesa todos los archivos PDF en un directorio."""
    processed = 0
    errors = 0
    
    # Asegurarse de que los directorios existan
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Buscando archivos PDF en {input_dir}...")
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No se encontraron archivos PDF para procesar.")
        return
    
    total_files = len(pdf_files)
    print(f"Encontrados {total_files} archivos PDF")
    
    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"\nProcesando archivo {idx}/{total_files}: {pdf_file}")
        
        if process_single_file(pdf_path, output_dir):
            processed += 1
        else:
            errors += 1
    
    print(f"\nResumen del procesamiento:")
    print(f"Archivos procesados exitosamente: {processed}")
    print(f"Archivos con errores: {errors}")
    print(f"Resultados guardados en: {output_dir}")

def show_menu():
    """Muestra el menú interactivo."""
    print("\nOCR PaddlePaddle - Procesador de documentos")
    print("============================================")
    print("\nTipos de PDF disponibles:")
    print("1. PDF Digital (texto seleccionable)")
    print("2. PDF Escaneado (imagen)")
    print("3. PDF Escrito a mano")
    print("4. Procesar directorio completo")
    print("5. Salir")
    
    while True:
        try:
            opcion = int(input("\nSeleccione una opción (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            else:
                print("Error: Por favor, seleccione una opción válida (1-5)")
        except ValueError:
            print("Error: Por favor, ingrese un número válido")

def main():
    # Configurar directorios
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, 'input_pdfs')
    output_dir = os.path.join(base_dir, 'output')
    
    # Crear directorios si no existen
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = {
        1: "pdf_digital.pdf",
        2: "pdf_escan.pdf",
        3: "pdf_escrito.pdf"
    }
    
    while True:
        opcion = show_menu()
        
        if opcion == 5:
            print("\n¡Hasta luego!")
            break
        elif opcion == 4:
            process_directory(input_dir, output_dir)
        else:
            pdf_file = pdf_files.get(opcion)
            if pdf_file:
                pdf_path = os.path.join(input_dir, pdf_file)
                if os.path.exists(pdf_path):
                    process_single_file(pdf_path, output_dir)
                else:
                    print(f"\nError: No se encontró el archivo {pdf_file} en {input_dir}")
            else:
                print("\nError: Opción no válida")

if __name__ == '__main__':
    main()
