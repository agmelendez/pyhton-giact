# 📤 GUÍA: SUBIR A GITHUB

## 🔧 Configuración Inicial

### Paso 0: Aceptar licencia Xcode (solo macOS)
```bash
sudo xcodebuild -license
# Lee y presiona 'q', luego responde 'agree'
```

---

## 📋 PASOS PARA SUBIR A GITHUB

### **Paso 1: Crear repositorio en GitHub**

1. Ve a: https://github.com/new
2. Completa:
   - **Repository name:** `guided-interface-marinos` (o tu nombre)
   - **Description:** "Guía interactiva: Técnicas en gestión marino-costera"
   - **Visibility:** Public (para que sea accesible)
   - **No** inicialices con README
3. Click: "Create repository"
4. **Copia la URL que te muestra** (HTTPS o SSH)

---

### **Paso 2: Configurar Git en tu máquina** (primera vez)

Si es tu **primera vez usando git**, configura:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

### **Paso 3: Inicializar Git en el proyecto**

En terminal, navega a la carpeta:

```bash
cd "/Users/agustingomez/Downloads/SPRINTS /Python/guided_interface"
```

Inicializa git:

```bash
git init
```

---

### **Paso 4: Agregar archivos**

```bash
git add .
```

---

### **Paso 5: Primer commit**

```bash
git commit -m "Initial commit: Guía interactiva de casos educativos marino-costeros"
```

---

### **Paso 6: Agregar repositorio remoto**

**Reemplaza `TU_USUARIO` y `TU_REPO` con tus valores:**

```bash
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
```

**Ejemplo real:**
```bash
git remote add origin https://github.com/agustingomez/guided-interface.git
```

---

### **Paso 7: Cambiar rama a 'main'**

```bash
git branch -M main
```

---

### **Paso 8: Subir a GitHub**

```bash
git push -u origin main
```

**Te pedirá autenticación:**
- Si usas HTTPS: usuario y contraseña (o token)
- Si usas SSH: deberías tener configurada tu clave

---

## ✅ Verificar que funcionó

```bash
# Ver remote configurado
git remote -v

# Ver archivos en git
git status
```

Deberías ver algo como:
```
On branch main
nothing to commit, working tree clean
```

---

## 🌐 Habilitar GitHub Pages

**Para que la interfaz sea accesible online:**

1. Ve a tu repositorio en GitHub
2. Click: **Settings** (arriba a la derecha)
3. Scroll a: **GitHub Pages**
4. **Branch:** selecciona `main`
5. **Folder:** selecciona `/ (root)`
6. Click: **Save**

Espera 1-2 minutos. Tu interfaz estará en:

```
https://TU_USUARIO.github.io/TU_REPO/
```

**Ejemplo:**
```
https://agustingomez.github.io/guided-interface/
```

---

## 🔗 Acceder a la Interfaz Online

Una vez en GitHub Pages:

```
https://TU_USUARIO.github.io/TU_REPO/index.html
```

¡Debería mostrar la interfaz completa funcionando!

---

## 🔄 Próximas actualizaciones

Después de esto, si haces cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

---

## ❓ Solución de Problemas

### "fatal: not a git repository"
```bash
git init
```

### "Permission denied (publickey)"
Configura SSH o usa HTTPS con token.

### "fatal: pathspec '.' did not match any files"
Asegúrate de estar en el directorio correcto:
```bash
pwd  # Debe mostrar la carpeta guided_interface
ls -la  # Debe mostrar index.html, cases.json, etc.
```

### "refused to merge unrelated histories"
```bash
git pull origin main --allow-unrelated-histories
```

---

## 📝 COMANDOS RÁPIDOS (Copia y pega)

### Primera vez (completo):
```bash
cd "/Users/agustingomez/Downloads/SPRINTS /Python/guided_interface"
sudo xcodebuild -license  # Escribe 'agree'
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
git init
git add .
git commit -m "Initial commit: Guía interactiva marino-costera"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

### Actualizaciones futuras:
```bash
cd "/Users/agustingomez/Downloads/SPRINTS /Python/guided_interface"
git add .
git commit -m "Tu mensaje"
git push
```

---

## 🎉 Resultado Final

Tu interfaz estará disponible en:

```
🌐 https://TU_USUARIO.github.io/TU_REPO/index.html
```

Y será accesible desde cualquier navegador en cualquier dispositivo. ✨

---

## 💡 Bonus: Actualizar README en GitHub

Copia el contenido de `GITHUB_README.md` al directorio raíz como `README.md`:

```bash
cp guided_interface/GITHUB_README.md README.md
git add README.md
git commit -m "Add GitHub README"
git push
```

---

¿Necesitas ayuda en algún paso específico? 🚀

