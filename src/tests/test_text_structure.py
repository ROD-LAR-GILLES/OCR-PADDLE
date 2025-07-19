import unittest
from src.ocr.postprocess import TextStructureAnalyzer, process_document_structure

class TestTextStructureAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextStructureAnalyzer()
        
    def test_title_detection(self):
        # Caso 1: Título principal
        titulo_principal = {
            'text': 'CAPÍTULO 1: INTRODUCCIÓN',
            'is_bold': True,
            'is_centered': True,
            'font_size': 16,
            'base_font_size': 10
        }
        self.assertTrue(self.analyzer.detect_title(titulo_principal))
        self.assertEqual(self.analyzer.get_hierarchy_level(titulo_principal), 1)
        
        # Caso 2: Subtítulo
        subtitulo = {
            'text': '1.1 Antecedentes',
            'is_bold': True,
            'is_centered': False,
            'font_size': 12,
            'base_font_size': 10
        }
        self.assertTrue(self.analyzer.detect_title(subtitulo))
        self.assertEqual(self.analyzer.get_hierarchy_level(subtitulo), 2)
        
        # Caso 3: Texto normal (no título)
        texto_normal = {
            'text': 'Este es un párrafo normal del documento que no debería ser detectado como título.',
            'is_bold': False,
            'is_centered': False,
            'font_size': 10,
            'base_font_size': 10
        }
        self.assertFalse(self.analyzer.detect_title(texto_normal))
        
    def test_document_structure(self):
        # Preparar documento de prueba
        documento = [
            {
                'text': 'SECCIÓN PRINCIPAL',
                'is_bold': True,
                'is_centered': True,
                'font_size': 18,
                'base_font_size': 10
            },
            {
                'text': '1. Subsección',
                'is_bold': True,
                'is_centered': False,
                'font_size': 14,
                'base_font_size': 10
            },
            {
                'text': 'Contenido normal del documento.',
                'is_bold': False,
                'is_centered': False,
                'font_size': 10,
                'base_font_size': 10
            }
        ]
        
        # Procesar estructura
        resultado = process_document_structure(documento)
        
        # Verificar resultados
        self.assertTrue(resultado[0]['is_title'])
        self.assertEqual(resultado[0]['hierarchy_level'], 1)
        self.assertTrue(resultado[1]['is_title'])
        self.assertEqual(resultado[1]['hierarchy_level'], 2)
        self.assertFalse(resultado[2]['is_title'])
        self.assertEqual(resultado[2]['hierarchy_level'], 0)

if __name__ == '__main__':
    unittest.main()
