# 🖥️ VISTA PREVIA DE LA INTERFAZ

## Lo que verás cuando abras `index.html`

---

## 1️⃣ ENCABEZADO (Header)

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  🌊 Guía interactiva: Técnicas y casos en gestión marino-costera          ║
║                                                                            ║
║  Repasa teoría, supuestos y práctica con ejemplos guiados a tu ritmo.     ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Elementos:**
- Título principal en azul marino
- Subtítulo descriptivo

---

## 2️⃣ LAYOUT PRINCIPAL

```
┌─────────────────────┬──────────────────────────────────────────────┐
│                     │                                              │
│   SIDEBAR           │          ÁREA PRINCIPAL                      │
│   (320 px)          │                                              │
│                     │                                              │
├─────────────────────┼──────────────────────────────────────────────┤
│ Casos / Técnicas    │ [Caso seleccionado]                         │
│                     │ 📁 Fuente: ...                              │
│ [✓] Árboles de      │                                              │
│     Decisión        │  ╭────────────────────────────────────────╮ │
│                     │  │ TEORÍA                                 │ │
│ [ ] PCA             │  │ ¿Qué es un Árbol de Decisión?         │ │
│                     │  │ Un árbol de decisiones es una...      │ │
│ [ ] K-Means         │  │                                        │ │
│                     │  │ (400+ palabras)                        │ │
│ [ ] ANOVA           │  │                                        │ │
│                     │  ╰────────────────────────────────────────╯ │
│                     │                                              │
│ ─────────────────── │  ╭────────────────────────────────────────╮ │
│ Secciones por caso: │  │ SUPUESTOS                              │ │
│ • Teoría            │  │ • Variables representativas            │ │
│ • Supuestos         │  │ • Tamaño muestral suficiente          │ │
│ • Práctica          │  │ • Independencia de observaciones       │ │
│ • Fragmentos        │  │ • Etiquetado de calidad                │ │
│ • Try it            │  ╰────────────────────────────────────────╯ │
│                     │                                              │
└─────────────────────┴──────────────────────────────────────────────┘
```

---

## 3️⃣ SECCIONES DE CONTENIDO (Scrolling hacia abajo)

### Sección: TEORÍA
```
╭────────────────────────────────────────────────────────────────────╮
│ 📖 TEORÍA                                                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ ¿Qué es un Árbol de Decisión?                                    │
│                                                                    │
│ Un árbol de decisiones es una herramienta de Machine Learning    │
│ utilizada para predecir el valor de una variable objetivo...     │
│                                                                    │
│ Se estructura como un árbol donde:                               │
│  • Nodo Raíz: punto de partida                                   │
│  • Nodos Internos: representan decisiones                        │
│  • Ramas: resultado de una decisión                              │
│  • Nodos Hoja: resultados finales                                │
│                                                                    │
│ [Continúa con 400+ palabras de teoría...]                        │
│                                                                    │
╰────────────────────────────────────────────────────────────────────╯
```

### Sección: SUPUESTOS
```
╭────────────────────────────────────────────────────────────────────╮
│ ✓ SUPUESTOS                                                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ • Variables representativas: Datos deben incluir todos los        │
│   factores ambientales relevantes                                 │
│                                                                    │
│ • Tamaño muestral: Suficientes observaciones por clase para      │
│   dividir adecuadamente                                           │
│                                                                    │
│ • Independencia: Observaciones independientes entre sí            │
│                                                                    │
│ • Etiquetado de calidad: Las etiquetas deben ser precisas        │
│                                                                    │
│ • No multicolinealidad perfecta: Evita degeneración en el árbol  │
│                                                                    │
╰────────────────────────────────────────────────────────────────────╯
```

### Sección: PRÁCTICA — Ejemplo paso a paso
```
╭────────────────────────────────────────────────────────────────────╮
│ 🔬 PRÁCTICA — Ejemplo paso a paso                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Paso 1: Preparación de Datos                                     │
│ Simulamos 100 observaciones de una región costera...             │
│                                                                    │
│ Paso 2: Dividir Datos                                            │
│ 80% entrenamiento, 20% prueba...                                 │
│                                                                    │
│ Paso 3: Entrenar Árbol de Decisión                               │
│ Usar max_depth=5 para evitar sobreajuste...                      │
│                                                                    │
│ Paso 4: Visualizar e Interpretar                                 │
│ Ver el árbol en forma visual...                                  │
│                                                                    │
│ Paso 5: Evaluar con Métricas                                     │
│ Precisión en entrenamiento vs prueba...                          │
│                                                                    │
│ Paso 6: Predicciones en Nuevos Datos                             │
│ Con nuevas observaciones...                                      │
│                                                                    │
╰────────────────────────────────────────────────────────────────────╯
```

### Sección: CÓDIGO PYTHON
```
╭────────────────────────────────────────────────────────────────────╮
│ 💻 Fragmento de código                                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ import pandas as pd                                 [Azul]       │
│ import numpy as np                                                │
│ from sklearn.tree import DecisionTreeClassifier     [Azul]       │
│                                                                    │
│ # Generar datos simulados (reproducible)                         │
│ np.random.seed(42)                                               │
│ n = 100                                             [Naranja]    │
│ temperatura = np.random.uniform(15, 30, n)                       │
│ salinidad = np.random.uniform(30, 40, n)                         │
│                                                                    │
│ # Crear variable objetivo basada en condiciones                  │
│ score = 0.5*temperatura + 0.3*salinidad - 0.2*pH + 0.1*nitratos │
│ quantiles = np.percentile(score, [33.3, 66.7])                   │
│ biodiversidad = pd.cut(score, bins=[-np.inf, ...])               │
│                                                                    │
│ [... 45-55 líneas más de código resaltado ...]                   │
│                                                                    │
│  ┌──────────────────────┬──────────────────────┐                │
│  │📥 Descargar (.py)   │📋 Copiar portapapeles│                │
│  └──────────────────────┴──────────────────────┘                │
│                                                                    │
╰────────────────────────────────────────────────────────────────────╯
```

### Sección: TRY IT — Instrucciones
```
╭────────────────────────────────────────────────────────────────────╮
│ 🧪 Try it — Instrucciones                                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Cómo ejecutar este ejemplo                                        │
│                                                                    │
│ 1. Requisitos: Python 3.8+, scikit-learn, pandas...              │
│                                                                    │
│ 2. Instalación de dependencias:                                  │
│    pip install scikit-learn pandas numpy matplotlib              │
│                                                                    │
│ 3. Pasos:                                                         │
│    - Abre el notebook SP-8502 · GIACT...                        │
│    - Ejecuta cada celda en orden (Ctrl+Enter)                    │
│    - En la celda de ejercicios, prueba diferentes valores        │
│                                                                    │
│ 4. Resultado esperado:                                           │
│    Un árbol visual, métricas de precisión, gráfico de            │
│    importancia de características                                │
│                                                                    │
│ Alternativa: Google Colab                                        │
│ Descarga el notebook y súbelo a colab.research.google.com        │
│                                                                    │
╰────────────────────────────────────────────────────────────────────╯
```

---

## 4️⃣ FOOTER (Pie)

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  Creado para la formación GIACT 2026 — interfaz de revisión y práctica.   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## 5️⃣ COMPORTAMIENTO INTERACTIVO

### Al hacer click en un botón de caso:
```
ANTES:                          DESPUÉS:
├─ [✓] Árboles de Decisión    ├─ [✓] Árboles de Decisión (azul)
├─ [ ] PCA                  →  ├─ [ ] PCA  
├─ [ ] K-Means                ├─ [ ] K-Means
└─ [ ] ANOVA                  └─ [ ] ANOVA

(El contenido a la derecha cambia instantáneamente)
```

### Al hacer click en "Copiar al portapapeles":
```
Botón muestra:
[📋 Copiar al portapapeles]  →  [✓ ¡Copiado!]  →  (2 segundos después)
                                                     [📋 Copiar al portapapeles]
```

### Al hacer click en "Descargar (.py)":
```
Descarga un archivo:
decision-trees.py
├─ Código completo
├─ 55 líneas
└─ Pronto para ejecutar en terminal
```

---

## 🎨 PALETA DE COLORES

```
Azul Principal (marino):     #0b67a3
├─ Encabezados
├─ Botones activos
└─ Enlaces

Fondo:                       #f8f9fa
├─ Área principal
└─ Paneles

Texto:                       #333333
└─ Legible, alto contraste

Código:                      #1e1e1e (fondo), colores sintaxis
├─ Keywords (azul)
├─ Strings (verde)
└─ Números (naranja)

Bordes:                      #ddd
└─ Separadores suaves
```

---

## 📱 RESPONSIVE (En móvil/tablet)

```
DESKTOP (>900px):           TABLET/MÓVIL (<900px):
┌─────┬────────────┐        ┌──────────────┐
│     │            │        │              │
│ S   │   MAIN     │   →    │   (vertical) │
│ I   │            │        │              │
│ D   │            │        ├──────────────┤
│ E   │            │        │              │
│ B   │            │        │   SIDEBAR    │
│ A   │            │        │              │
│ R   │            │        │              │
│     │            │        │              │
└─────┴────────────┘        └──────────────┘

320px + flex            100% ancho
```

---

## ⌨️ ATAJOS Y CONTROLES

| Acción | Efecto |
|--------|--------|
| F12 | Abrir consola (ver logs de diagnóstico) |
| Ctrl+F5 | Recarga completa (limpia caché) |
| Scroll | Navegar entre secciones |
| Click botón | Cambiar caso |
| Click descarga | Guardar código como .py |
| Click copiar | Copiar código al portapapeles |

---

## 🎯 EXPERIENCIA DEL USUARIO

### Flujo típico:

1. **Cargar página** (1-2 segundos)
   - Encabezado aparece
   - Botones se cargan
   - Primer caso se carga automáticamente

2. **Explorar teoría** (1-2 minutos)
   - Lee Teoría
   - Revisa Supuestos
   - Sigue Práctica

3. **Estudiar código** (2-3 minutos)
   - Lee código resaltado
   - Copia o descarga

4. **Experimentar** (5+ minutos)
   - Abre Jupyter/Colab
   - Ejecuta ejemplos
   - Modifica parámetros

5. **Cambiar caso** (vuelve a paso 2)

---

## ✨ CARACTERÍSTICAS VISUALES

✓ Diseño limpio y moderno  
✓ Colores consistentes  
✓ Espaciado generoso (evita aglomeración)  
✓ Código resaltado con colores  
✓ Botones con hover effects  
✓ Transiciones suaves  
✓ Tipografía legible  
✓ Contraste adecuado  
✓ Responsive en todos los tamaños  
✓ Accesible (navegación por teclado)  

---

## 🖱️ INTERACTIVIDAD

- ✅ Botones hover (cambio de color)
- ✅ Click para cambiar casos
- ✅ Scroll suave
- ✅ Transiciones CSS
- ✅ Efectos de feedback
- ✅ Animaciones no intrusivas

---

## 📊 ESTADÍSTICAS VISUALES

```
Tamaño interfaz: ~100% ancho del navegador
Altura típica: 2000-3000px (requiere scroll)

Distribución:
├─ Header: 120px
├─ Teoría: 600px
├─ Supuestos: 300px
├─ Práctica: 400px
├─ Código: 500px
├─ Try It: 300px
└─ Footer: 60px
```

---

## 🎓 CASOS VISIBLES

Cuando abras la interfaz, verás estos 4 casos disponibles:

1. ✅ **Árboles de Decisión** (Seleccionado por defecto)
   - Predicción de biodiversidad marina

2. **PCA**
   - Análisis de datos oceanográficos

3. **K-Means**
   - Segmentación de hábitats marinos

4. **ANOVA**
   - Comparación entre regiones costeras

Puedes cambiar entre ellos haciendo click en los botones del sidebar izquierdo.

---

**🖥️ ¡Así se ve la interfaz! Moderna, limpia, pedagógica y completamente funcional.**

