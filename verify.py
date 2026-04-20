#!/usr/bin/env python3
"""
Script de verificación de la interfaz de casos
Valida que todos los archivos existan y estén configurados correctamente
"""

import os
import json
import sys

def check_files():
    """Verifica que existen los archivos necesarios"""
    required_files = {
        'index.html': 'Interfaz principal',
        'styles.css': 'Estilos CSS',
        'cases.json': 'Datos de casos',
    }
    
    print("🔍 Verificando archivos necesarios...\n")
    all_ok = True
    
    for filename, description in required_files.items():
        if os.path.exists(filename):
            size_kb = os.path.getsize(filename) / 1024
            print(f"  ✓ {filename:20} ({size_kb:6.1f} KB) — {description}")
        else:
            print(f"  ✗ {filename:20} NO ENCONTRADO — {description}")
            all_ok = False
    
    return all_ok

def check_json():
    """Verifica que cases.json es válido"""
    print("\n🔍 Verificando integridad de cases.json...\n")
    
    try:
        with open('cases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'cases' not in data:
            print("  ✗ JSON válido pero NO tiene clave 'cases'")
            return False
        
        num_cases = len(data['cases'])
        print(f"  ✓ JSON válido — {num_cases} casos encontrados:\n")
        
        for i, case in enumerate(data['cases'], 1):
            required_keys = ['id', 'title', 'source', 'theory', 'assumptions', 
                           'practice', 'code', 'tryit']
            
            case_ok = all(key in case for key in required_keys)
            status = "✓" if case_ok else "✗"
            
            title = case.get('title', 'SIN TÍTULO')[:50]
            print(f"    {status} Caso {i}: {title}...")
            
            if not case_ok:
                missing = [k for k in required_keys if k not in case]
                print(f"       Faltan: {missing}")
        
        return num_cases > 0
        
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON INVÁLIDO: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def check_html():
    """Verifica que index.html tiene estructura correcta"""
    print("\n🔍 Verificando estructura HTML...\n")
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        checks = {
            '<h1>' in html: 'Título H1',
            'id="case-list"' in html: 'Contenedor de casos (#case-list)',
            'id="theory"' in html: 'Sección de teoría',
            'id="code-snippet"' in html: 'Sección de código',
            'document.addEventListener' in html: 'Event listener DOMContentLoaded',
            'cases.json' in html: 'Referencia a cases.json',
            'hljs' in html: 'Highlight.js incluido',
        }
        
        all_ok = True
        for check, description in checks.items():
            status = "✓" if check else "✗"
            print(f"  {status} {description}")
            if not check:
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def check_css():
    """Verifica que styles.css existe y tiene contenido"""
    print("\n🔍 Verificando estilos CSS...\n")
    
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            css = f.read()
        
        size_lines = len(css.split('\n'))
        
        checks = {
            ':root' in css: 'Variables CSS (colores)',
            '.container' in css: 'Clase .container',
            '.sidebar' in css: 'Clase .sidebar',
            '.panel' in css: 'Clase .panel',
            'flexbox' in css or 'display: flex' in css: 'Diseño flexbox',
        }
        
        print(f"  ✓ CSS válido ({size_lines} líneas)\n")
        
        all_ok = True
        for check, description in checks.items():
            status = "✓" if check else "✗"
            print(f"    {status} {description}")
            if not check:
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Ejecuta todas las verificaciones"""
    print("\n" + "="*70)
    print("  ✨ VERIFICACIÓN DE INTERFAZ DE CASOS")
    print("="*70 + "\n")
    
    results = {
        'Archivos': check_files(),
        'JSON': check_json(),
        'HTML': check_html(),
        'CSS': check_css(),
    }
    
    print("\n" + "="*70)
    print("  📊 RESUMEN")
    print("="*70 + "\n")
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status:8} — {name}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("\n  ✅ ¡TODO VERIFICADO! La interfaz está lista para usar.\n")
        print("  Próximos pasos:")
        print("  1. Abre terminal en este directorio")
        print("  2. Ejecuta: python3 -m http.server 8000")
        print("  3. Abre: http://localhost:8000/index.html\n")
        return 0
    else:
        print("\n  ⚠️ Hay problemas. Por favor revisa los errores arriba.\n")
        print("  Requisitos:")
        print("  - index.html, styles.css, cases.json en el mismo directorio")
        print("  - JSON válido en cases.json")
        print("  - Python 3.8+ para servidor local\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())

