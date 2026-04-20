# Interfaz Guiada Interactiva — Técnicas para la Gestión Marino-Costera

Esta es una interfaz web estática (HTML + CSS + JSON) pensada como **guía pedagógica interactiva** que explica para cada caso/técnica:
- **Teoría:** conceptos clave y marcos teóricos
- **Supuestos:** condiciones para aplicar el método
- **Práctica:** ejemplo paso a paso con datos reales
- **Código:** fragmento Python completo y ejecutable
- **Try It:** instrucciones para ejecutar en tu propia máquina

---

## 🚀 Cómo Usar

### Opción 1: Abrir localmente (Recomendado)
1. Descarga la carpeta `guided_interface` o clona el repositorio.
2. Abre el archivo `index.html` con tu navegador (doble-clic o arrastra a navegador).
3. Selecciona un caso en la columna izquierda.
4. Lee la teoría, supuestos y práctica.
5. Descarga el código o copia al portapapeles para experimentar.

### Opción 2: Servidor local (para debugging)
```bash
cd guided_interface
python3 -m http.server 8000
# Abre http://localhost:8000 en navegador
```

---

## 📚 Casos Incluidos

1. **Árboles de Decisión** — Clasificación y predicción en gestión marino-costera
   - Predicción de biodiversidad basada en variables ambientales
   - Ejemplo: clasificación de hábitats por temperatura, salinidad, pH

2. **PCA (Análisis de Componentes Principales)** — Reducción dimensional
   - Exploración de múltiples variables oceanográficas
   - Ejemplo: análisis de 8 variables para 20 estaciones marinas

3. **K-Means Clustering** — Segmentación de hábitats
   - Identificación de regiones homogéneas
   - Ejemplo: agrupación de 50 sitios por características ambientales

4. **ANOVA** — Comparación de medias entre grupos
   - Test de hipótesis para múltiples regiones/períodos
   - Ejemplo: biodiversidad en 3 regiones costeras

---

## 🛠 Características

✅ **Interfaz limpia y moderna** — navegación intuitiva  
✅ **Código con resaltado de sintaxis** — Python-ready copy/paste  
✅ **Descargar snippets** — exporta fragmentos como archivos .py  
✅ **Respuesta educativa** — teoría → supuestos → práctica → código  
✅ **Instrucciones ejecutables** — "Try It" con pasos claros  

---

## 📖 Estructura de Archivos

```
guided_interface/
├── index.html              # Página principal (abrir en navegador)
├── styles.css              # Estilos (diseño limpio y responsivo)
├── cases.json              # Contenido de todos los casos (teoría, código, etc.)
├── extract_text.py         # Utilidad para extraer texto de .docx/.pptx
├── requirements.txt        # Dependencias Python para extractor
├── extracted/              # Archivos .txt extraídos desde documentos
│   ├── Guia_Laboratorios_Python_GIACT_2026.txt
│   └── Metodos_Analisis_Cuantitativo.txt
└── README.md               # Este archivo
```

---

## 🔧 Dependencias para el Extractor

El archivo `extract_text.py` extrae contenido de la guía Word y presentación PowerPoint. Para usarlo:

```bash
pip install -r requirements.txt
python3 extract_text.py
```

Esto genera archivos `.txt` en la carpeta `extracted/` que se usaron para crear el contenido de los casos.

---

## 💻 Requisitos del Sistema

- **Navegador moderno** (Chrome, Firefox, Safari, Edge)
- **Python 3.8+** (solo si ejecutas los ejemplos de código)
- **Bibliotecas Python** (al ejecutar cada ejemplo):
  - `scikit-learn` — machine learning
  - `pandas` — manipulación de datos
  - `numpy` — cálculos numéricos
  - `matplotlib` / `seaborn` — visualización
  - `scipy` — estadística

---

## 🎓 Uso Pedagógico

### Para Estudiantes
1. Selecciona un caso que corresponda a tu módulo.
2. Lee primero la **Teoría** para entender conceptos.
3. Revisa los **Supuestos** para ver cuándo aplicar.
4. Sigue el **Práctica** paso a paso.
5. Copia o descarga el **Código** y experimenta.
6. Ejecuta según las instrucciones **Try It**.

### Para Instructores
- Personaliza `cases.json` con tus propios ejemplos.
- Añade más casos copiando la estructura de un caso existente.
- Comparte el archivo `index.html` con estudiantes (funciona offline).
- Embebe en tu LMS o plataforma de aprendizaje.

---

## 📝 Personalización

Para añadir un nuevo caso, edita `cases.json` y añade un objeto con esta estructura:

```json
{
  "id": "mi-tecnica",
  "title": "Mi Técnica — Aplicación",
  "source": "notebook_fuente.ipynb",
  "theory": "<p>Descripción teórica...</p>",
  "assumptions": "<ul><li>Supuesto 1</li>...</ul>",
  "practice": "<h4>Paso 1:...</h4><p>...</p>",
  "code": "import pandas as pd\n# código aquí",
  "tryit": "<h4>Cómo ejecutar:</h4><ol>...</ol>"
}
```

---

## 🔗 Recursos Vinculados

- **Notebooks Jupyter:** Todos los archivos `.ipynb` en el workspace contienen ejemplos completos
- **Google Colab:** Los ejemplos funcionan directamente en [Colab](https://colab.research.google.com)
- **Guía de Laboratorios:** Ver `Guia_Laboratorios_Python_GIACT_2026.docx` para contexto completo

---

## 🐛 Soporte

- Verifica que `cases.json` tenga sintaxis JSON válida (usa [JSONLint](https://jsonlint.com))
- Si el código no se resalta, verifica que el navegador carga el CDN de highlight.js
- Para ejecutar código, asegúrate de tener las dependencias Python instaladas

---

## 📜 Licencia

Contenido creado para el curso **Métodos de Análisis Cuantitativo — Python Aplicado a Ciencias Marino-Costeras** (GIACT 2026).

---

**Creado con ❤️ para facilitar el aprendizaje de técnicas de análisis cuantitativo en contextos marino-costeros.**