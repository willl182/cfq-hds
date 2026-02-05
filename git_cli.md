# Guía Práctica de GitHub CLI y Git

> Guía para dejar de depender del navegador en operaciones de GitHub usando el comando `gh`

## Quickstart: Crear Tu Primer Repositorio

Si ya tienes un proyecto con commits y quieres crear el repositorio GitHub **sin abrir el navegador**:

```bash
# 1. Autenticar con GitHub (primera vez)
gh auth login --git-protocol ssh

# 2. Crear repositorio desde directorio actual
gh repo create cfq-hds --private --source=. --remote=origin --push

# 3. Verificar que se creó correctamente
gh repo view
```

**Resultado**: Tu repositorio ya existe en GitHub con todos los commits locales sincronizados. 🚀

---

## 1. Instalación y Verificación

### Verificar si está instalado

```bash
gh --version
git --version
```

**Salida esperada**:
```
gh version 2.x.x
git version 2.x.x
```

### Instalación rápida

**Linux (Ubuntu/Debian)**:
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update
sudo apt install gh
```

**macOS (Homebrew)**:
```bash
brew install gh
```

**Windows**:
- Descargar instalador desde https://cli.github.com/

---

## 2. Autenticación con GitHub

### 2.1 Primer Autenticación (método SSH - Recomendado)

```bash
gh auth login --git-protocol ssh
```

**Qué sucede**:
1. Abre el navegador para que autorices la aplicación
2. GitHub detecta automáticamente tu llave SSH
3. El token de autenticación se guarda localmente
4. Git se configura para usar SSH por defecto

### 2.2 Configuración SSH (una sola vez)

#### Paso 1: Verificar llaves existentes

```bash
ls -la ~/.ssh/
```

**Busca**: `id_rsa.pub`, `id_ed25519.pub`, o similar

#### Paso 2: Generar llave si no existe

```bash
# Genera llave Ed25519 (más segura)
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
```

**Preguntas durante generación**:
- Guardar en: `/home/w182/.ssh/id_ed25519` (default)
- Contraseña: puede dejarla vacía (enter en blanco)

#### Paso 3: Agregar llave a GitHub

```bash
# Copia el contenido de tu llave pública
cat ~/.ssh/id_ed25519.pub

# Método 1: Desde CLI (si tienes la llave en archivo)
gh ssh-key add ~/.ssh/id_ed25519.pub

# Método 2: Desde GitHub.com (más visual)
# 1. Ve a https://github.com/settings/keys
# 2. Click en "New SSH key"
# 3. Pega el contenido de id_ed25519.pub
```

#### Paso 4: Probar conexión

```bash
# Test de conexión a GitHub
ssh -T git@github.com
```

**Éxito**: `Hi usuario! You've successfully authenticated, but GitHub does not provide shell access.`

### 2.3 Verificar estado de autenticación

```bash
gh auth status
```

**Salida esperada**:
```
github.com
  Logged in to github.com account tu-usuario (key: SHA256:abcd...)
  - Git protocol: ssh
  - Active account: true
```

### 2.4 Reautenticar (si el token expiró)

```bash
gh auth logout --hostname github.com
gh auth login --git-protocol ssh
```

---

## 3. Operaciones de Repositorios

### 3.1 Crear repositorio nuevo (vacío)

```bash
# Interactivo (te pregunta nombre, tipo, etc.)
gh repo create

# No interactivo - recomendado para automatización
gh repo create nombre-repo \
  --private \
  --description "Descripción del repositorio" \
  --source=. \           # Usa directorio actual como fuente
  --remote=origin \       # Nombre del remoto
  --push                 # Sube commits inmediatamente
```

**Flags útiles**:
- `--public`: Repositorio público
- `--license MIT`: Agrega licencia
- `--gitignore Python`: Agrega .gitignore para Python

### 3.2 Crear repositorio desde directorio existente ← TU CASO

Cuando ya tienes un proyecto con commits:

```bash
gh repo create cfq-hds \
  --private \
  --source=. \
  --remote=origin \
  --push \
  --description "Sistema de Hojas de Seguridad para fertilizantes Calferquim"
```

**Qué hace cada flag**:
- `--source=.`: Lee el directorio actual como proyecto
- `--remote=origin`: Configura `origin` como remoto
- `--push`: Sube todos los commits existentes inmediatamente

### 3.3 Clonar repositorio existente

```bash
gh repo clone usuario/nombre-repo
cd nombre-repo
```

### 3.4 Listar tus repositorios

```bash
gh repo list
```

### 3.5 Ver información de un repositorio

```bash
# Ver repositorio actual
gh repo view

# Ver repositorio específico
gh repo view usuario/otro-repo
```

---

## 4. Flujo de Trabajo Diario

### 4.1 Ciclo básico de commits

```bash
# 1. Agregar archivos al área de staging
git add archivo1.py archivo2.md

# 2. Crear commit con mensaje claro
git commit -m "Agregar scripts de generación HDS"

# 3. Subir cambios a GitHub
git push origin main
```

**Mejor práctica**: Mensajes de commit con formato

```bash
# ✅ Bueno - Describe qué y por qué
git commit -m "feat: agregar motor de combinación GHS para mezclas"

# ❌ Malo - No explica nada
git commit -m "actualizar archivos"
```

### 4.2 Ver estado y cambios

```bash
# Estado del directorio de trabajo
git status

# Ver qué cambió entre commits
git diff HEAD~1
git diff origin/main  # Comparar con remoto
```

### 4.3 Sincronizar con remoto

```bash
# Traer cambios del remoto
git pull origin main

# Traer sin fusionar (revisar primero)
git fetch origin
git log origin/main  # Ver commits remotos
```

### 4.4 Crear y cambiar de rama

```bash
# Crear nueva rama
git checkout -b feature/generacion-pdfs

# Cambiar a rama existente
git checkout develop

# Listar todas las ramas
git branch -a
```

### 4.5 Fusionar ramas (merge)

```bash
# Cambiar a rama destino (main)
git checkout main

# Fusionar feature en main
git merge feature/generacion-pdfs

# Subir resultado
git push origin main
```

### 4.6 Historial de commits

```bash
# Ver últimos 10 commits
git log --oneline -10

# Ver con gráfico
git log --graph --oneline -10
```

---

## 5. Git Worktrees (Trabajo en Paralelo)

### 5.1 ¿Qué son y cuándo usarlos?

Un **worktree** permite tener múltiples copias del mismo repositorio en diferentes directorios, cada una en una rama diferente.

**Casos de uso**:
- Trabajar en un hotfix urgente mientras desarrollas una feature
- Revisar una rama antigua sin perder tu trabajo actual
- Tener múltiples versiones desplegadas en paralelo

### 5.2 Crear worktree para otra rama

```bash
# Escenario: Trabajas en feature/hds-system y llega un bug en producción

# Crear worktree para hotfix (se crea en directorio ../cfq_hds-hotfix)
git worktree add ../cfq_hds-hotfix main

# Cambiar al worktree
cd ../cfq_hds-hotfix

# Arreglar bug, hacer commit, push
git commit -m "fix: resolver error en validación de pictogramas"
git push origin main

# Regresar al directorio original
cd ../cfq_hds
```

### 5.3 Listar worktrees activos

```bash
git worktree list
```

**Salida**:
```
/path/to/cfq_hds-hotfix  abc1234 [main]
```

### 5.4 Eliminar worktree cuando termines

```bash
# Primero asegurarte de estar fuera del worktree
cd /path/to/cfq_hds

# Eliminar worktree
git worktree remove /path/to/cfq_hds-hotfix
```

⚠️ **No elimines el directorio manualmente**: el comando también lo borra del sistema git.

### 5.5 Caso práctico desde OpenCode

Si estás trabajando en `/home/w182/w421/cfq_hds` (rama `feature/hds`):

```bash
# Necesitas crear un hotfix en rama `main`
git worktree add ../cfq_hds-hotfix main

# Cambia al hotfix, arreglar, commitear
cd ../cfq_hds-hotfix
# ... trabajo en hotfix ...
git push origin main

# Vuelve a tu trabajo original sin cambios perdidos
cd ../cfq_hds
git worktree remove ../cfq_hds-hotfix
# Ahora sigues en feature/hds donde lo dejaste
```

---

## 6. Issues desde CLI

### 6.1 Crear un issue

```bash
# Básico - te pide título y cuerpo
gh issue create

# Con flags (recomendado)
gh issue create "Error en combinación de pictogramas" \
  --body "### Descripción

Al generar HDS para mezclas con más de 5 componentes, se duplican pictogramas.

### Pasos para reproducir
1. Crear receta con 6 componentes
2. Ejecutar: ./scripts/generar_hds.py --pt
3. Ver etiqueta generada

**Resultados esperados**
- Máximo 5 pictogramas según SGA

**Resultado actual**
- Se muestran 6 pictogramas (duplicados)" \
  --label "bug" \
  --repo cfq-hds
```

**Flags útiles**:
- `--label`: Agrega etiquetas (bug, enhancement, documentation)
- `--assignee`: Asigna a alguien
- `--web`: Abre el issue en el navegador después de crearlo

### 6.2 Listar issues

```bash
# Ver todos los issues
gh issue list

# Ver issues abiertos
gh issue list --state open

# Ver issues cerrados recientes
gh issue list --state closed --limit 10
```

### 6.3 Ver issue específico

```bash
# Por número
gh issue view 42

# Por título
gh issue view --repo cfq-hds "Error en combinación"
```

### 6.4 Cerrar issue

```bash
# Con número
gh issue close 42 --comment "Solucionado en commit abc123"

# Con referencia
gh issue close --comment "Implementado en #45"
```

---

## 7. Pull Requests desde CLI

### 7.1 Crear un Pull Request

```bash
# Estás en rama feature/generacion-pdfs y quieres fusinar en main

gh pr create \
  --title "Agregar generación de PDFs" \
  --body "### Cambios

Esta PR agrega funcionalidad para convertir Markdown a PDF directamente desde el script.

### Testing
- Probado con 3 productos terminados
- PDFs generados correctamente

### Checklist
- [x] Script modificado
- [x] Pruebas realizadas
- [x] Documentación actualizada" \
  --base main \
  --head feature/generacion-pdfs
```

**Qué significan los flags**:
- `--base main`: Rama donde se fusionará (destino)
- `--head feature/...`: Tu rama actual (origen)

### 7.2 Listar Pull Requests

```bash
# Ver todas las PRs
gh pr list

# Ver PRs abiertas
gh pr list --state open

# Ver PRs específicas de un repositorio
gh pr list --repo cfq-hds
```

### 7.3 Ver detalles de una PR

```bash
# Por número
gh pr view 15

# Ver archivos cambiados
gh pr diff 15

# Ver estado (checks, revisiones)
gh pr checks 15
```

### 7.4 Fusionar una PR (desde CLI)

```bash
gh pr merge 15 --merge --delete-branch
```

**Resultado**: La rama se fusiona y se borra automáticamente con `--delete-branch`.

### 7.5 Revisar cambios de una PR

```bash
# Cambiar al trabajo de la PR
gh pr checkout 15

# Volver a tu rama original
git checkout main
```

---

## 8. Comandos Útiles

### 8.1 Abrir en navegador

```bash
# Abrir repositorio actual
gh browse

# Abrir issue específico
gh browse --repo cfq-hds issues/42

# Abrir pull request
gh browse --repo cfq-hds pull/15
```

### 8.2 Crear gists (fragmentos de código rápidos)

```bash
# Desde archivo
gh gist create script.py --desc "Script de combinación GHS"

# Desde texto inline
echo "print('Hola')" | gh gist create
```

### 8.3 Crear alias (atajos)

```bash
# Crear alias para comando frecuente
gh alias set sync='git pull origin main && git push origin main'

# Usar alias
gh sync
```

### 8.4 Ver repositorio en formato web

```bash
gh repo view --web
```

### 8.5 Buscar repositorios

```bash
# Buscar por nombre
gh search cfq-hds

# Buscar por lenguaje
gh search language:python stars:>10

# Buscar por temas
gh search topics:fertilizantes
```

---

## 9. Cheatsheet (Referencia Rápida)

| Acción | Comando | Ejemplo |
|---------|---------|---------|
| **Autenticación** |
| Ver estado | `gh auth status` | Verificas que estás logueado |
| Login | `gh auth login` | Primera vez |
| Logout | `gh auth logout` | Cerrar sesión |
| **Repositorios** |
| Crear (vacío) | `gh repo create nombre-repo` | Nuevo proyecto |
| Crear (existente) | `gh repo create --source=. --push` | Tu caso actual |
| Clonar | `gh repo clone usuario/repo` | Copiar a local |
| Listar | `gh repo list` | Ver todos los tuyos |
| Ver info | `gh repo view` | Detalles del repo |
| **Flujo Git** |
| Estado | `git status` | Cambios pendientes |
| Agregar | `git add archivo` | Staging |
| Commit | `git commit -m "mensaje"` | Guardar cambios |
| Subir | `git push origin main` | Sincronizar |
| Traer | `git pull origin main` | Actualizar local |
| Diferencias | `git diff` | Ver cambios |
| **Worktrees** |
| Crear | `git worktree add ../nombre rama` | Hotfix paralelo |
| Listar | `git worktree list` | Ver activos |
| Eliminar | `git worktree remove ruta` | Limpiar |
| **Issues** |
| Crear | `gh issue create "Título" --body "Desc"` | Reportar bug |
| Listar | `gh issue list` | Ver issues |
| Ver | `gh issue view 42` | Detalles |
| Cerrar | `gh issue close 42` | Resolver |
| **Pull Requests** |
| Crear | `gh pr create --base main` | Proponer cambios |
| Listar | `gh pr list` | Ver PRs |
| Ver | `gh pr view 15` | Detalles |
| Fusionar | `gh pr merge 15` | Aprobar |
| **Útiles** |
| Abrir | `gh browse` | Navegador |
| Gist | `gh gist create archivo.py` | Compartir código |
| Buscar | `gh search termino` | Encontrar repos |

---

## 10. Solución de Problemas Comunes

### 10.1 Token inválido o expirado

**Error**:
```
The token in default is invalid.
```

**Solución**:
```bash
gh auth logout
gh auth login --git-protocol ssh
```

### 10.2 Permission denied (SSH)

**Error**:
```
Permission denied (publickey).
```

**Causas comunes**:
1. La llave no se agregó a GitHub
2. Usas un usuario incorrecto
3. El agente SSH no usa la llave correcta

**Solución**:
```bash
# 1. Verificar llave usada
ssh-add -l  # Lista llaves cargadas en el agente

# 2. Re-agregar llave a GitHub (si no aparece en GitHub.com/settings/keys)
gh ssh-key add ~/.ssh/id_ed25519.pub
```

### 10.3 Conflictos de merge

**Error al hacer `git pull`:
```
CONFLICT (content): Merge conflict in archivo.py
```

**Solución**:
1. Abre el archivo con conflictos (busca `<<<<<<<` y `>>>>>>>`)
2. Resuelve manualmente las diferencias
3. Marca como resuelto:
```bash
git add archivo.py
git commit -m "resolve: conflicto de merge en archivo.py"
git push origin main
```

### 10.4 Worktree bloqueado

**Error**:
```
fatal: worktree at '/path/to/worktree' is locked, reason: 'hotfix urgente'
```

**Solución**:
```bash
# Desbloquear
git worktree unlock /path/to/worktree --reason "hotfix urgente"

# O eliminar worktree forzado
git worktree remove /path/to/worktree
```

### 10.5 Rama ya existe en remoto

**Error al hacer `git push`:
```
! [rejected] main -> main (fetch first)
```

**Solución**:
```bash
git fetch origin
git pull origin main --rebase
git push origin main
```

---

## Apéndice: Configuración Inicial de Git

Solo necesitas hacer esto **una vez**:

```bash
# Configurar nombre y email (obligatorio para commits)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@dominio.com"

# Configurar editor por defecto
git config --global core.editor "code --wait"

# Configurar ramificación por defecto
git config --global init.defaultBranch main
```

---

## Recursos Adicionales

- **Documentación oficial**: https://cli.github.com/manual
- **Git Book**: https://git-scm.com/book/es/v2
- **GitHub Docs**: https://docs.github.com/es

---

**Versión de la guía**: 1.0
**Última actualización**: 2026-02-04
**Compatible con**: GitHub CLI 2.x+, Git 2.x+
