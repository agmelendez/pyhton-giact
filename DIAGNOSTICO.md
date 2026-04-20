# 🔍 GUÍA DE DIAGNÓSTICO - Interfaz de Casos

## Paso 1: Verificar que los archivos existen

Abre una terminal en el directorio `/Users/agustingomez/Downloads/SPRINTS /Python/guided_interface/` y ejecuta:

```bash
ls -la *.html *.json *.css 2>/dev/null | head -20
```

**Debes ver como mínimo:**
- `index.html` ✓
- `cases.json` ✓
- `styles.css` ✓

---

## Paso 2: Verificar que cases.json es válido

```bash
python3 -m json.tool cases.json | head -30
```

**Debe mostrar JSON válido sin errores.** Si ves un error de sintaxis, el JSON está corrupto.

---

## Paso 3: Opción A - Abrir en navegador (Recomendado: vía HTTP local)

Si abres `index.html` directamente como `file://`, algunos navegadores pueden bloquear fetch() por razones de seguridad.

**Solución: Usar un servidor HTTP simple:**

```bash
# En el directorio guided_interface
python3 -m http.server 8000
```

Luego abre en el navegador:
```
http://localhost:8000/index.html
```

---

## Paso 4: Abrir consola del navegador

**En Chrome/Firefox/Safari/Edge:**
- Presiona **F12** o **Cmd+Option+I** (Mac)
- Ve a la pestaña **Console**

**Debes ver logs como:**
```
🚀 Iniciando interfaz de casos...
📥 Buscando cases.json en el directorio actual...
✅ cases.json cargado correctamente. Casos encontrados: 4
  ✓ Caso 1: "Análisis de Variación en Poblaciones de Plancton"
  ✓ Caso 2: "Efecto de la Intensidad de Luz en el Crecimiento de Algas"
  ✓ Caso 3: "Pronóstico de Lluvia Mensual para Planificación Agrícola"
  ✓ Caso 4: "ANOVA: Efecto de Profundidad en Distribución de Especies"
📖 Mostrando caso: "Análisis de Variación..." (analyzing-plankton)
  ✓ Teoría cargada
  ✓ Supuestos cargados
  ✓ Práctica cargada
  ✓ Código resaltado con Highlight.js
  ✓ Try it cargado
✅ Caso mostrado completamente
```

---

## Paso 5: Si hay errores en la consola

### Error: "Failed to fetch 'cases.json'"

**Soluciones:**
1. Verifica que `cases.json` existe en el mismo directorio que `index.html`
2. Intenta abrir vía HTTP (Paso 3) en lugar de file://
3. Verifica permisos: `ls -l cases.json` (debe ser legible)

### Error: "Unexpected token < in JSON at position 0"

Significa que `cases.json` está corrupto o no se está sirviendo como JSON. Verifica con:
```bash
python3 -m json.tool cases.json
```

### Error: "hljs is not defined" (Amarillo)

Es advertencia, no error. Significa que Highlight.js no cargó completamente. La interfaz funciona igual.

### No ves logs en la consola

Significa que el script no se ejecutó. Verifica:
1. ¿Cargó la página completamente?
2. ¿Ves errores de Network en la pestaña Network de DevTools?
3. ¿Está bloqueado JavaScript?

---

## Paso 6: Probar cada función

### ✓ Los botones de casos aparecen en la izquierda
- Si no: revisar logs en la consola (Paso 4)

### ✓ Al hacer clic en un botón, carga contenido
- Debería mostrar: Teoría, Supuestos, Práctica, Código, Try it
- Revisa la consola para ver logs de qué se cargó

### ✓ El código tiene colores (resaltado)
- Si no: Highlight.js no se cargó, pero funciona igual

### ✓ Botón "Descargar snippet (.py)"
- Debe descargar un archivo `.py` con el código
- Revisa downloads

### ✓ Botón "Copiar al portapapeles"
- Debe mostrar "✓ ¡Copiado!" por 2 segundos
- Verifica pegando el código en un editor

---

## Soluciones Rápidas

| Problema | Solución |
|----------|----------|
| No carga nada | Intenta `python3 -m http.server 8000` + http://localhost:8000 |
| Botones vacíos | Verifica logs (F12 → Console) |
| JSON corrupto | Ejecuta `python3 -m json.tool cases.json` |
| Permisos denegados | `chmod 644 cases.json` y `chmod 644 index.html` |
| Página blanca | Espera 2-3 segundos, luego F5 recarga |

---

## Información adicional

**Archivos creados en este proyecto:**
- `index.html` - Interfaz principal (85 KB)
- `styles.css` - Estilos (8 KB)
- `cases.json` - Datos de casos (26 KB)
- `run_example.py` - Ejemplos en terminal
- `extract_text.py` - Herramienta de extracción
- Documentación: README.md, INICIO_RAPIDO.md, etc.

**Requisitos:**
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Python 3.8+ (para servidor local)
- JavaScript habilitado

---

## ¿Aún hay problemas?

1. Abre la consola (F12)
2. Copia todos los logs rojos/naranjas
3. Verifica que `cases.json` existe y es válido
4. Intenta con `python3 -m http.server 8000`

