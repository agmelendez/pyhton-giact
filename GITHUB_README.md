# 🌊 Guía Interactiva: Técnicas y Casos en Gestión Marino-Costera

Una interfaz web educativa interactiva con 4 casos de estudio completos para enseñanza de técnicas de análisis cuantitativo aplicadas a gestión marino-costera.

**[🔗 Abre la interfaz aquí (haz clic)](https://[tu-usuario].github.io/[tu-repo]/index.html)**

---

## ✨ Características

✅ **Interfaz web moderna y responsiva**  
✅ **4 casos de estudio completos** con teoría, supuestos, práctica y código  
✅ **Código Python ejecutable** (207+ líneas)  
✅ **Teoría académica rigurosa** (1,600+ palabras)  
✅ **Práctica paso a paso** (27+ pasos)  
✅ **Código resaltado con colores** (Highlight.js)  
✅ **Sin dependencias complejas** — solo HTML/CSS/JSON  
✅ **Completamente verificado y funcional**  

---

## 🎓 Casos Incluidos

### 1. Árboles de Decisión
**Predicción de Biodiversidad Marina**
- Teoría sobre algoritmos de decisión
- Aplicación en gestión costera
- Código de ejemplo con scikit-learn
- 55 líneas de Python ejecutable

### 2. PCA — Análisis de Componentes Principales
**Reducción Dimensional de Datos Oceanográficos**
- Conceptos de transformación ortogonal
- Scree plots y biplots
- Aplicación en análisis multivariante
- 52 líneas de código con visualización

### 3. K-Means Clustering
**Segmentación de Hábitats Marinos**
- Algoritmo de clustering no supervisado
- Método del codo para k óptimo
- Silhouette score para evaluación
- 48 líneas de Python

### 4. ANOVA
**Comparación de Medias Entre Grupos**
- Hipótesis estadísticas
- Prueba F y post-hoc
- Comparación de regiones costeras
- 52 líneas con Shapiro, Levene, Tukey

---

## 🚀 Cómo Usar

### Opción 1: En GitHub Pages (Recomendado)
1. Fork o copia este repositorio
2. Activa GitHub Pages en Settings
3. Abre: `https://[tu-usuario].github.io/[nombre-repo]/index.html`

### Opción 2: Localmente
```bash
# Clonar
git clone https://github.com/[tu-usuario]/[tu-repo].git
cd [tu-repo]

# Iniciar servidor local
python3 -m http.server 8000

# Abrir navegador
http://localhost:8000/index.html
```

---

## 📁 Estructura del Proyecto

```
guided_interface/
├── 🎯 INTERFAZ (ARCHIVOS PRINCIPALES)
│   ├── index.html              ← Interfaz web (abrir esto)
│   ├── styles.css              ← Estilos CSS
│   └── cases.json              ← Datos de 4 casos (26 KB)
│
├── 🔧 HERRAMIENTAS
│   ├── verify.py               ← Script de verificación
│   ├── run_example.py          ← Ejecutor de ejemplos
│   ├── extract_text.py         ← Extractor de Office
│   └── start.sh                ← Script para servidor
│
├── 📖 DOCUMENTACIÓN
│   ├── COMENZAR_AQUI.md        ← Quick start
│   ├── ESTADO_DEL_PROYECTO.md  ← Estado actual
│   ├── DIAGNOSTICO.md          ← Solución de problemas
│   ├── RESUMEN_FINAL.md        ← Resumen completo
│   └── [+8 documentos más]
│
└── 📁 extracted/               ← Textos extraídos
```

---

## 🎯 Funcionalidades

### Para Estudiantes
- 📖 Lee teoría rigurosa
- 📋 Sigue práctica paso a paso
- 💻 Copia código Python
- 📥 Descarga ejemplos

### Para Instructores
- 🎓 Enseña de forma interactiva
- 🔄 Los estudiantes exploran a su ritmo
- 🎨 Interfaz profesional y moderna
- 📊 4 casos educativos completos

### Para Investigadores
- 🔬 Código reproducible
- 📚 Documentación integrada
- 🎯 Ejemplos contextualizados
- 💾 Descargar y adaptar

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| **Archivos totales** | 25 |
| **Tamaño total** | ~310 KB |
| **Casos completos** | 4 |
| **Líneas código Python** | 207+ |
| **Palabras teoría** | 1,600+ |
| **Pasos práctica** | 27+ |
| **Verificación** | ✅ Pasada |

---

## ✅ Verificación Rápida

```bash
# Verificar que todo funciona
python3 verify.py

# Deberías ver:
# ✓ PASS — Archivos
# ✓ PASS — JSON
# ✓ PASS — HTML
# ✓ PASS — CSS
# ✅ ¡TODO VERIFICADO!
```

---

## 🌍 Acceso Online (GitHub Pages)

1. **Habilita GitHub Pages:**
   - Ve a Settings → Pages
   - Selecciona rama `main`
   - Guarda

2. **Accede a:**
   ```
   https://[tu-usuario].github.io/[nombre-repo]/
   ```

3. **¡La interfaz se cargará automáticamente!**

---

## 💻 Requisitos

- ✅ Navegador moderno (Chrome, Firefox, Safari, Edge)
- ✅ JavaScript habilitado
- ✅ Conexión a Internet (para Highlight.js CDN)

**No requiere:**
- ❌ Node.js
- ❌ Backend
- ❌ Base de datos
- ❌ Instalación compleja

---

## 📖 Documentación

Toda la documentación está incluida. Comienza por:

- **[COMENZAR_AQUI.md](guided_interface/COMENZAR_AQUI.md)** — Quick start (5 min)
- **[ESTADO_DEL_PROYECTO.md](guided_interface/ESTADO_DEL_PROYECTO.md)** — Estado actual
- **[DIAGNOSTICO.md](guided_interface/DIAGNOSTICO.md)** — Troubleshooting
- **[INDICE.md](guided_interface/INDICE.md)** — Índice completo de documentación

---

## 🔗 Enlaces Rápidos

- 🌐 [Interfaz Web](index.html)
- 📚 [Documentación Completa](guided_interface/INDICE.md)
- 🔧 [Verificador](guided_interface/verify.py)
- 📊 [Casos (JSON)](guided_interface/cases.json)

---

## 🎓 Contexto Educativo

Proyecto creado para **GIACT 2026** — Programa de Formación en Técnicas de Análisis Cuantitativo para Gestión Marino-Costera.

**Objetivo:** Proporcionar una interfaz educativa moderna que integre teoría, supuestos, práctica y código ejecutable para enseñanza de técnicas multivariantes.

---

## 📝 Licencia

[Tu licencia aquí — ej: MIT, CC-BY-4.0, etc.]

---

## 👨‍💻 Contribuciones

¿Quieres agregar más casos? 

1. Fork el repositorio
2. Edita `guided_interface/cases.json`
3. Agrega un nuevo caso siguiendo la estructura existente
4. Pull request

---

## 📞 Soporte

- 📖 Abre [DIAGNOSTICO.md](guided_interface/DIAGNOSTICO.md) para troubleshooting
- 🔍 Verifica que `cases.json` está en el mismo directorio que `index.html`
- 🌐 Usa `python3 -m http.server 8000` para servir localmente
- 💬 Abre un Issue si encuentras problemas

---

## 🎉 Estado

🟢 **COMPLETAMENTE FUNCIONAL Y VERIFICADO**

- ✅ Interfaz operacional
- ✅ 4 casos incluidos
- ✅ Documentación exhaustiva
- ✅ 0 errores críticos
- ✅ Listo para producción

---

**¡Disfruta explorando técnicas de gestión marino-costera!** 🌊
