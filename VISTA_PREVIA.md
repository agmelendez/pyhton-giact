# 👁️ VISTA PREVIA DE LA INTERFAZ

Esto es lo que verás cuando abras `index.html` en tu navegador:

---

## PANTALLA PRINCIPAL (Desktop)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
│                                                                         │
│  🌊 Guía interactiva: Técnicas y casos en gestión marino-costera       │
│     Repasa teoría, supuestos y práctica con ejemplos guiados a tu ritmo.│
│                                                                         │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
├────────────────────┬─────────────────────────────────────────────────┤
│                    │                                                   │
│  CASOS/TÉCNICAS    │  Árboles de Decisión — Gestión Marino-Costera   │
│  ┌──────────────┐  │  📁 Fuente: SP-8502 · GIACT_Teoría_y_...        │
│  │ • Árboles de │  │                                                   │
│  │   Decisión ✓ │  │  📚 TEORÍA                                       │
│  └──────────────┘  │  ─────────────────────────────────────────────   │
│  ┌──────────────┐  │  ¿Qué es un Árbol de Decisión?                   │
│  │ • PCA        │  │                                                   │
│  └──────────────┘  │  Un árbol de decisiones es una herramienta de    │
│  ┌──────────────┐  │  Machine Learning utilizada para predecir...    │
│  │ • K-Means    │  │                                                   │
│  └──────────────┘  │  [contenido detallado]                           │
│  ┌──────────────┐  │                                                   │
│  │ • ANOVA      │  │  ✅ SUPUESTOS                                    │
│  └──────────────┘  │  ─────────────────────────────────────────────   │
│                    │  • Variables representativas                     │
│  SECCIONES         │  • Tamaño muestral suficiente                    │
│  ─────────────────  │  • Independencia                                │
│  • Teoría          │  • Etiquetado de calidad                         │
│  • Supuestos       │                                                   │
│  • Práctica        │  🔨 PRÁCTICA                                     │
│  • Fragmentos      │  ─────────────────────────────────────────────   │
│  • Try it          │  Ejemplo Paso a Paso: [...]                     │
│                    │                                                   │
│                    │  💻 FRAGMENTO DE CÓDIGO                          │
│                    │  ─────────────────────────────────────────────   │
│                    │  import pandas as pd                              │
│                    │  import numpy as np                               │
│                    │  from sklearn.tree import DecisionTreeClassifier  │
│                    │  # Código completo aquí...                        │
│                    │  [DESCARGAR] [COPIAR AL PORTAPAPELES]            │
│                    │                                                   │
│                    │  ℹ️ TRY IT — INSTRUCCIONES                       │
│                    │  ─────────────────────────────────────────────   │
│                    │  Cómo ejecutar este ejemplo [...]                │
│                    │                                                   │
├────────────────────┴─────────────────────────────────────────────────┤
│ 📝 Creado para la formación GIACT 2026 — interfaz de revisión y prác │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ELEMENTOS INTERACTIVOS

### 1. Botones de Casos (Sidebar)

```
[• Árboles de Decisión]  ← Clickeable, con hover azul marino
[• PCA]
[• K-Means]
[• ANOVA]
```

Efecto al clickear:
- El caso se resalta
- El contenido principal se actualiza
- Se carga la teoría, supuestos, práctica y código del caso

### 2. Botones de Código

```
┌─────────────────────────────────────────┐
│ [🔽 Descargar snippet (.py)]            │ ← Descarga el código
│ [📋 Copiar al portapapeles]             │ ← Copia a clipboard
└─────────────────────────────────────────┘
```

Feedback:
- Al copiar: botón cambia a "✓ Copiado!" por 2 segundos
- Al descargar: abre diálogo de descarga

### 3. Resaltado de Código

```python
import pandas as pd                    ← Resaltado en colores
import numpy as np                     ← Sintaxis Python
from sklearn.tree import DecisionTreeClassifier

# Generar datos simulados            ← Comentarios en verde
np.random.seed(42)                     ← Números en cian
```

---

## SECCIONES DE CONTENIDO

### Teoría
- Explicación conceptual (300-500 palabras)
- Definiciones de componentes clave
- Aplicaciones en gestión marino-costera
- Ventajas y desventajas

### Supuestos
- Lista punteada (3-5 items)
- Condiciones necesarias para aplicar el método
- Referencias a cuándo revisar

### Práctica
- Procedimiento paso a paso (5-8 pasos)
- Descripciones detalladas
- Referencias a variables y conceptos
- Subpasos cuando es necesario

### Código
- Python 3.8+ completo
- Comentarios explicativos
- Imports listos
- Datos simulados con random_state=42
- Visualizaciones incluidas

### Try It
- Instrucciones para ejecutar
- Requisitos de librerías
- Múltiples opciones (local, Colab, terminal)
- Resultado esperado

---

## PALETA DE COLORES

```
Fondo principal:     #f5f7fa (gris claro)
Tarjetas:            #ffffff (blanco)
Texto principal:     #111827 (gris oscuro)
Acento primario:     #0b67a3 (azul marino)
Acento oscuro:       #084a73 (azul marino oscuro)
Texto muted:         #6b7280 (gris medio)
Borde:               #e5e7eb (gris claro)
Código bg:           #0f1724 (azul muy oscuro)
Código texto:        #e6eef6 (gris claro)
```

---

## COMPORTAMIENTO RESPONSIVO

### Desktop (> 900px)
```
Sidebar | Contenido principal
300px   | Flexible
```
- Dos columnas
- Sidebar fijo a la izquierda

### Tablet (600-900px)
```
Sidebar arriba (botones horizontales)
────────────────────────────────────
Contenido principal debajo
```
- Una columna
- Navegación horizontal

### Móvil (< 600px)
```
Menú desplegable (⋮)
Contenido a pantalla completa
```
- Una columna
- Menú comprimido

---

## ANIMACIONES Y TRANSICIONES

1. **Botones de caso**
   - Hover: fondo azul marino, color blanco
   - Transición: 0.2s smooth
   - Active: escala 0.98 (presionado)

2. **Botones de acción**
   - Hover: sombra aumenta, color más oscuro
   - Click: feedback visual (cambio de texto)

3. **Cambio de contenido**
   - La página se scrollea al inicio (smooth)
   - Contenido nuevo aparece sin animación

4. **Resaltado de código**
   - Sintaxis coloreada al cargar
   - Transición suave (instantánea)

---

## ACCESIBILIDAD

- ✓ Semántica HTML5 correcta
- ✓ Contraste de colores WCAG AA
- ✓ Tamaños de fuente legibles
- ✓ Espaciado generoso
- ✓ Botones con aria-labels implícitos

---

## FLUJO DE USUARIO TÍPICO

1. **Abre index.html**
   - Página carga en 1-2 segundos
   - Cases se cargan desde cases.json
   - Primer caso (Árboles de Decisión) se selecciona por defecto

2. **Explora Teoría**
   - Lee la sección con background azul claro
   - Entiende conceptos clave

3. **Revisa Supuestos**
   - Ve lista de condiciones
   - Verifica si su caso cumple requisitos

4. **Sigue Práctica**
   - Lee paso a paso
   - Entiende el flujo del análisis

5. **Examina Código**
   - Ve código Python resaltado
   - Lee comentarios

6. **Elige acción**
   - Descarga como .py
   - O copia al portapapeles
   - O abre en Colab

7. **Ejecuta en Python**
   - Sigue instrucciones "Try It"
   - Corre el código
   - Experimenta modificando

8. **Aprende iterativamente**
   - Vuelve a la interfaz
   - Lee documentación
   - Experimenta

---

## CASOS DE USO

### Caso 1: Abriendo por primera vez
- Usuario hace doble-clic en index.html
- Ve interfaz con primer caso cargado
- Lee la teoría
- Descarga código

### Caso 2: Navegando entre técnicas
- Usuario hace clic en "PCA" en sidebar
- Contenido se actualiza dinámicamente
- Ve ejemplo PCA con 8 variables oceanográficas

### Caso 3: Ejecutando código
- Usuario copia código del botón
- Lo pega en Jupyter o IDE
- Ejecuta con datos de ejemplo

### Caso 4: Trabajando offline
- Usuario abre index.html localmente
- Funciona 100% offline
- Solo resaltado de código requeriría internet

---

## INFORMACIÓN DE DEBUGGING

Si algo no funciona:

1. **Código no aparece de color**
   - Verificar que CDN Highlight.js carga
   - Abrir consola (F12) y buscar errores

2. **Casos no cargan**
   - Verificar cases.json es válido
   - Abrir consola para ver errores de JSON

3. **Botones no funcionan**
   - Verificar JavaScript está habilitado
   - Mirar consola del navegador (F12)

4. **Estilos no se aplican**
   - Verificar que styles.css está en la misma carpeta
   - Hard refresh (Ctrl+Shift+R)

---

## PRÓXIMAS PANTALLAS (Opcional)

Se podrían agregar:

- [ ] Página de inicio con intro de 10 segundos
- [ ] Cuestionarios post-lectura
- [ ] Progreso visual (X% completado)
- [ ] Certificado de finalización
- [ ] Chat bot con preguntas
- [ ] Notebook embebido (Jupyter incrustado)

---

**¡Eso es todo! La interfaz es completamente intuitiva y lista para usar.**

Ahora abre `index.html` en tu navegador y comienza. 🚀
