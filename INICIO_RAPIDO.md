# 🚀 INICIO RÁPIDO

Bienvenido a la **Guía Interactiva: Técnicas para la Gestión Marino-Costera**

## Paso 1: Abrir la Interfaz Web (Lo Más Fácil)

**Opción A: Doble-clic directo**
1. En tu computadora, ve a `/Users/agustingomez/Downloads/SPRINTS /Python/guided_interface/`
2. Haz doble-clic en `index.html`
3. Se abrirá en tu navegador por defecto

**Opción B: Arrastra a navegador**
1. Abre tu navegador (Chrome, Firefox, Safari, etc.)
2. Arrastra el archivo `index.html` a la ventana del navegador

**✅ Resultado esperado:**
- Ves un título "Guía interactiva: Técnicas y casos en gestión marino-costera"
- En la columna izquierda tienes una lista de casos (Árboles de Decisión, PCA, K-Means, ANOVA)
- Al hacer clic en un caso, ves la teoría, supuestos, práctica y código

---

## Paso 2: Explorar un Caso

1. Haz clic en **"Árboles de Decisión"** (primer caso)
2. Lee la sección de Teoría para entender conceptos
3. Revisa Supuestos para ver cuándo aplicar la técnica
4. Sigue la Práctica paso a paso
5. Ve el código Python completo en "Fragmento de código"
6. Usa los botones:
   - **Descargar snippet (.py)** → descarga el código como archivo Python
   - **Copiar al portapapeles** → copia el código para pegar en tu IDE

---

## Paso 3: Ejecutar el Código en Python

### Requisito: Instalar librerías
Abre una terminal/consola y ejecuta:

```bash
pip install scikit-learn pandas numpy matplotlib scipy seaborn
```

### Opción A: Usando Jupyter (Recomendado para estudiantes)

1. Abre el notebook original en Jupyter:
   ```bash
   jupyter notebook '/Users/agustingomez/Downloads/SPRINTS /Python/SP-8502 · GIACT_Teoría_y_Aplicación_del_Árbol_de_Decisiones_en_la_Gestión_Marino_Costera.ipynb'
   ```

2. Ejecuta celda por celda (Shift+Enter)

3. Experimenta: modifica valores y vuelve a ejecutar

### Opción B: Usar el ejecutor interactivo

1. En terminal, ve a la carpeta `guided_interface`:
   ```bash
   cd '/Users/agustingomez/Downloads/SPRINTS /Python/guided_interface'
   ```

2. Ejecuta:
   ```bash
   python3 run_example.py
   ```

3. Sigue el menú interactivo:
   - Selecciona un ejemplo (1-4)
   - Elige ejecutar o descargar
   - El código correrá en la terminal

### Opción C: Google Colab (Sin instalar nada)

1. Ve a https://colab.research.google.com
2. Sube el notebook correspondiente (Archivo → Subir cuaderno)
3. Ejecuta las celdas
4. Todo funciona en la nube

---

## Paso 4: Modificar y Experimentar

Una vez tengas el código ejecutándose:

1. **Cambia los datos**: modifica valores de entrada
2. **Ajusta parámetros**: prueba diferentes valores (ej. max_depth en árboles)
3. **Observa cambios**: ejecuta de nuevo y compara resultados
4. **Crea nuevo código**: combina fragmentos de diferentes casos

---

## Contenidos Disponibles

### 📊 4 Casos Principales

| Caso | Tema | Aplicación Marina |
|------|------|-------------------|
| **Árboles de Decisión** | Clasificación supervisada | Predicción de biodiversidad, clasificación de hábitats |
| **PCA** | Reducción dimensional | Análisis de múltiples variables oceanográficas |
| **K-Means** | Clustering no-supervisado | Segmentación de hábitats y regiones marinas |
| **ANOVA** | Contraste de hipótesis | Comparación de medias entre regiones/períodos |

Cada caso incluye:
✓ Teoría (conceptos clave)
✓ Supuestos (cuándo usar)
✓ Práctica (ejemplo paso a paso)
✓ Código (Python completo)
✓ Try It (instrucciones de ejecución)

---

## 📚 Archivos Importantes

```
guided_interface/
├── 🌐 index.html              ← ABRE ESTO EN NAVEGADOR
├── 🎨 styles.css              (estilos, no tocar)
├── 📋 cases.json              (contenido de casos, puedes editar)
├── 📖 README.md               (documentación completa)
├── 🐍 run_example.py          (ejecutor interactivo)
├── extract_text.py            (extrae de documentos)
├── requirements.txt           (dependencias Python)
└── extracted/                 (archivos extraídos)
```

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito instalar algo?**
R: Solo si quieres ejecutar el código Python. La interfaz web abre directamente sin instalación.

**P: ¿Cómo añado más casos?**
R: Edita `cases.json` y sigue la estructura de un caso existente. Recarga `index.html`.

**P: ¿Puedo usar esto offline?**
R: Sí, excepto que necesitarás internet para el resaltado de código (CDN Highlight.js). Si no tienes internet, elimina la línea del CDN en `index.html`.

**P: ¿Qué hago si el código no funciona?**
R: Verifica que instalaste todas las librerías: `pip install -r guided_interface/requirements.txt`

**P: ¿Puedo compartir esta interfaz?**
R: Sí, comparte la carpeta `guided_interface` completa. Funciona en cualquier navegador.

---

## 🎯 Flujo de Aprendizaje Sugerido

1. **Día 1:** Lee Teoría + Supuestos de Árboles de Decisión
2. **Día 2:** Ejecuta el código del árbol, experimenta con parámetros
3. **Día 3:** Lee y ejecuta PCA
4. **Día 4:** Lee y ejecuta K-Means
5. **Día 5:** Lee y ejecuta ANOVA
6. **Semana 2:** Combina técnicas en un proyecto propio

---

## 📞 Próximos Pasos

- **Personalización:** edita `cases.json` para añadir tus propios casos
- **Integración:** embebe `index.html` en un LMS (Canvas, Moodle, etc.)
- **Extensión:** conecta con Jupyter notebooks o Google Colab
- **Más casos:** hay 20 notebooks en el workspace; podemos convertir más

---

**¡Bienvenido! Estamos listos para aprender. Abre `index.html` en tu navegador. 🚀**
