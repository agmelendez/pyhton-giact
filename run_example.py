#!/usr/bin/env python3
"""
Ejecutor de ejemplos interactivo para la guía de técnicas marino-costeras.

Uso:
  python3 run_example.py

Te permitirá seleccionar un ejemplo y ejecutar su código.
"""

import json
import sys
from pathlib import Path

def load_cases():
    """Carga los casos desde cases.json"""
    cases_file = Path(__file__).parent / 'cases.json'
    if not cases_file.exists():
        print(f"❌ Archivo {cases_file} no encontrado.")
        sys.exit(1)
    with open(cases_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['cases']

def show_menu(cases):
    """Muestra menú de selección"""
    print("\n" + "="*70)
    print("📊 GUÍA INTERACTIVA — Técnicas para Gestión Marino-Costera")
    print("="*70)
    print("\nSelecciona un ejemplo para ver y ejecutar:\n")
    for i, case in enumerate(cases, 1):
        print(f"  {i}. {case['title']}")
    print(f"  0. Salir")
    print("\n" + "-"*70)

def show_case_detail(case):
    """Muestra detalles de un caso"""
    print("\n" + "="*70)
    print(f"📖 {case['title']}")
    print("="*70)
    print(f"\nFuente: {case.get('source', 'No especificada')}\n")

    # Mostrar teoría (primera 500 chars)
    print("📚 TEORÍA (resumen):")
    print("-" * 70)
    theory_text = case.get('theory', '').replace('<h4>', '\n✓ ').replace('</h4>', '\n')
    theory_text = theory_text.replace('<p>', '').replace('</p>', '\n')
    theory_text = theory_text.replace('<ul>', '').replace('</ul>', '')
    theory_text = theory_text.replace('<li>', '  • ').replace('</li>', '')
    theory_text = theory_text.replace('<em>', '').replace('</em>', '')
    theory_text = theory_text.replace('<strong>', '').replace('</strong>', '')
    print(theory_text[:600] + "..." if len(theory_text) > 600 else theory_text)

    # Mostrar supuestos
    print("\n\n✅ SUPUESTOS:")
    print("-" * 70)
    assumptions_text = case.get('assumptions', '')
    assumptions_text = assumptions_text.replace('<ul>', '').replace('</ul>', '')
    assumptions_text = assumptions_text.replace('<li>', '  • ').replace('</li>', '')
    assumptions_text = assumptions_text.replace('<strong>', '').replace('</strong>', '')
    print(assumptions_text)

    # Mostrar código
    print("\n\n💻 CÓDIGO:")
    print("-" * 70)
    code = case.get('code', '# Código no disponible')
    lines = code.split('\n')
    # Mostrar primeras 20 líneas
    for i, line in enumerate(lines[:20], 1):
        print(f"{i:3d} | {line}")
    if len(lines) > 20:
        print(f"... ({len(lines) - 20} líneas más)")

def run_example(case):
    """Intenta ejecutar el código del ejemplo"""
    code = case.get('code', '')
    if not code:
        print("\n❌ No hay código disponible para este caso.")
        return

    print("\n" + "="*70)
    print("⚙️  EJECUTANDO CÓDIGO...")
    print("="*70 + "\n")

    try:
        exec(code)
    except ImportError as e:
        print(f"\n❌ Falta instalar: {e}")
        print("\nInstala las dependencias necesarias con:")
        print("  pip install scikit-learn pandas numpy matplotlib scipy seaborn")
    except Exception as e:
        print(f"\n❌ Error durante ejecución: {e}")
        import traceback
        traceback.print_exc()

def export_code(case):
    """Exporta el código a un archivo"""
    code = case.get('code', '')
    if not code:
        print("\n❌ No hay código disponible para exportar.")
        return

    filename = f"{case['id']}.py"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"\n✓ Código exportado a: {filename}")

def main():
    """Función principal"""
    cases = load_cases()

    while True:
        show_menu(cases)
        try:
            choice = input("Selecciona opción (número): ").strip()
            if choice == '0':
                print("\n👋 ¡Hasta pronto!\n")
                break
            
            idx = int(choice) - 1
            if 0 <= idx < len(cases):
                case = cases[idx]
                show_case_detail(case)

                print("\n" + "-"*70)
                print("¿Qué deseas hacer?")
                print("  1. Ejecutar el código")
                print("  2. Descargar el código (.py)")
                print("  3. Volver al menú")
                print("-"*70)

                action = input("Elige acción (1-3): ").strip()
                if action == '1':
                    run_example(case)
                    input("\nPresiona Enter para continuar...")
                elif action == '2':
                    export_code(case)
                    input("\nPresiona Enter para continuar...")
            else:
                print("\n❌ Opción no válida. Intenta de nuevo.")
        except ValueError:
            print("\n❌ Por favor, ingresa un número válido.")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!\n")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

if __name__ == '__main__':
    main()
