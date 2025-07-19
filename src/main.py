import os
import argparse
from pathlib import Path
from ocr.processor import process_document
from utils.pdf_to_images import convert_pdf_to_images

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
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_ocr.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
            
        print(f"Archivo procesado exitosamente: {output_path}")
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

def main():
    parser = argparse.ArgumentParser(description='OCR PaddlePaddle - Procesador de documentos')
    parser.add_argument('--file', '-f', help='Procesar un archivo PDF específico')
    parser.add_argument('--input-dir', '-i', default='input_pdfs', 
                      help='Directorio de entrada con archivos PDF (por defecto: input_pdfs)')
    parser.add_argument('--output-dir', '-o', default='output',
                      help='Directorio de salida para los resultados (por defecto: output)')
    
    args = parser.parse_args()
    
    # Convertir rutas relativas a absolutas
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, args.input_dir)
    output_dir = os.path.join(base_dir, args.output_dir)
    
    print("OCR PaddlePaddle - Procesador de documentos")
    print("============================================")
    
    # Crear directorios si no existen
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    if args.file:
        # Modo archivo único
        if os.path.isabs(args.file):
            pdf_path = args.file
        else:
            pdf_path = os.path.join(input_dir, args.file)
        
        if not os.path.exists(pdf_path):
            print(f"Error: El archivo {pdf_path} no existe")
            return
        
        process_single_file(pdf_path, output_dir)
    else:
        # Modo directorio completo
        process_directory(input_dir, output_dir)

if __name__ == '__main__':
    main()
