# Guía Práctica de GitHub CLI y Git

> Guía completa para dejar de depender del navegador en operaciones de GitHub usando el comando `gh`

## 0. Prerrequisitos

Antes de empezar, necesitas:

- Una cuenta en [GitHub.com](https://github.com)
- Un sistema Linux con terminal
- Conexión a internet

### 0.1 Verificar si ya tienes cuenta

Ve a [github.com/settings/keys](https://github.com/settings/keys) para verificar si ya tienes llaves SSH configuradas.

---

## 1. Instalación (Linux/Ubuntu/Debian)

### 1.1 Instalar Git

```bash
# Actualizar paquetes
sudo apt update

# Instalar Git
sudo apt install git
```

**Salida esperada**:
```
git version 2.x.x
```

### 1.2 Instalar GitHub CLI (gh)

```bash
# Agregar repositorio de GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

# Configurar repositorio
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list

# Actualizar e instalar
sudo apt update
sudo apt install gh
```

**Salida esperada**:
```
gh version 2.x.x
```

### 1.3 Verificar instalación

```bash
# Verificar versión de Git
git --version

# Verificar versión de GitHub CLI
gh --version
```

---

## 2. Configuración Inicial de Git (UNA VEZ)

Solo necesitas hacer esto **la primera vez**. Configura tu nombre y email para los commits.

```bash
# Configurar nombre de usuario para commits
git config --global user.name "Tu Nombre Apellido"

# Configurar email de usuario para commits
git config --global user.email "tu-email@dominio.com"

# Configurar editor por defecto (opcional)
git config --global core.editor "code --wait"

# Configurar rama por defecto (main, no master)
git config --global init.defaultBranch main
```

**Salida esperada**:
No hay error (el comando no muestra nada)

### 2.1 Verificar configuración

```bash
# Ver toda la configuración
git config --global --list
```

**Salida esperada**:
```
user.name=Tu Nombre Apellido
user.email=tu-email@dominio.com
init.defaultbranch=main
core.editor=code --wait
```

### 2.2 Cambiar de 'master' a 'main' (Opcional)

Si Git creó por defecto una rama llamada `master` y prefieres usar `main` (el estándar actual):

```bash
# 1. Renombrar la rama local actual de master a main
git branch -m master main

# 2. Configurar Git para que use 'main' en todos los repositorios nuevos
git config --global init.defaultBranch main
```

**Salida esperada**:
No hay error. Puedes verificar el cambio con:
```bash
git branch
```
→ Debería mostrar `* main` en lugar de `master`.

---

## 3. Crear Llave SSH (ANTES de Autenticarse)

### 3.1 Verificar si ya tienes llave SSH

```bash
ls -la ~/.ssh/
```

**Si existe una llave** (verás algo así):
```
drwx------  2 usuario usuario 4096 Feb  3 00:27 .
-rw-------  1 usuario usuario  411 Feb  3 00:27 id_ed25519
-rw-r--r--  1 usuario usuario   97 Feb  3 00:27 id_ed25519.pub
```
→ Ya tienes llave, salta al paso 3.3

**Si NO existe** (verás esto):
```
ls: cannot access '/home/usuario/.ssh': No such file or directory
```
→ Continúa al paso 3.2

### 3.2 Generar nueva llave SSH

```bash
# Generar llave Ed25519 (más segura y moderna)
ssh-keygen -t ed25519 -C "tu-email@dominio.com"
```

**Interacción completa**:
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/w182/.ssh/id_ed25519): 
```
→ Presiona ENTER para usar ubicación por defecto

```
Enter passphrase (empty for no passphrase):
```
→ Escribe una contraseña O presiona ENTER dos veces (o déjalo vacío)

```
Your identification has been saved in /home/w182/.ssh/id_ed25519
Your public key has been saved in /home/w182/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:abc123def456... tu-email@dominio.com
The key's randomart image is:
+--[ED25519 256]--+
|                 |
|     E    .      |
|    + .oo+ o     |
|     X BS.= o    |
| . =.*.== =     |
|.o==.oo..   .    |
| o=.+.o+o.   +   |
|.o==.oo..   .    |
+----[SHA256]-----+
```

### 3.3 Verificar que se creó la llave

```bash
# Verificar archivos creados
ls ~/.ssh/
```

**Salida esperada**:
```
drwx------  2 usuario usuario Feb  3 00:27 .
-rw-------  1 usuario usuario Feb  3 00:27 id_ed25519
-rw-r--r--  1 usuario usuario   97 Feb  3 00:27 id_ed25519.pub
```

### 3.4 Verificar contenido de la llave pública

```bash
# Ver la llave pública (solo primera línea)
head -3 ~/.ssh/id_ed25519.pub
```

**Salida esperada**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... tu-email@dominio.com
```

---

## 4. Autenticarse con GitHub CLI

### 4.1 Ejecutar el comando de autenticación

```bash
gh auth login
```

### 4.2 Elegir host

**Pregunta del CLI**:
```
? Where do you use GitHub?  [Use arrows to move, type to filter]
> GitHub.com
```
→ Selecciona `GitHub.com` (si ya está seleccionado, presiona ENTER)

### 4.3 Elegir protocolo

**Pregunta del CLI**:
```
? What is your preferred protocol for Git operations on this host?  [Use arrows to move, type to filter]
> SSH
```
→ Selecciona `SSH` con las flechas (↑↓) y presiona ENTER

### 4.4 Subir la llave SSH

**Pregunta del CLI**:
```
? Upload your SSH public key to your GitHub account?  [Use arrows to move, type to filter]
> /home/w182/.ssh/id_ed25519.pub
  Skip
```
→ Selecciona tu archivo `.pub` y presiona ENTER

### 4.5 Dar nombre a la llave

**Pregunta del CLI**:
```
? Title for your SSH key? (GitHub CLI)
```
→ Escribe un nombre descriptivo: `mi-laptop-linux` o `workstation` o `desktop`

**Nota**: Este nombre es SOLO una etiqueta, NO afecta la seguridad.

### 4.6 Código de autenticación

**Pregunta del CLI**:
```
! First copy your one-time code: AB12-CD34
Press Enter to open github.com in your browser...
```
→ Presiona ENTER para abrir el navegador

### 4.7 Autorizar en el navegador

En el navegador que se abre:

1. El código ya debe estar autocompletado
2. Click en **Authorize**
3. (Opcional) Escribe una nota: "Linux - generada para GitHub CLI"
4. Click en **Continue**

### 4.8 Verificar autenticación en la terminal

**De vuelta en la terminal**:
```
✓ Authentication complete.
✓ Configured git protocol to ssh
✓ Uploaded to SSH key to your GitHub account: /home/w182/.ssh/id_ed25519.pub
✓ Logged in as tu-usuario
```

### 4.9 Probar conexión SSH a GitHub

```bash
# Test de conexión
ssh -T git@github.com
```

**Salida esperada**:
```
Hi tu-usuario! You've successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed by remote host.
```

### 4.10 Verificar estado de autenticación

```bash
gh auth status
```

**Salida esperada**:
```
github.com
  Logged in to github.com account tu-usuario (key: SHA256:abc...)
  - Git protocol: ssh
  - Active account: true
```

---

## 5. Quickstart: Crear Tu Primer Repositorio

### 5.1 Opción A: Crear repositorio NUEVO (vacío)

Si NO tienes un proyecto:

```bash
# Crear repositorio y clonarlo en una sola línea
gh repo create cfq-hds \
  --private \
  --description "Sistema de Hojas de Seguridad para fertilizantes Calferquim" \
  --clone

# Cambiar al directorio del repositorio
cd cfq-hds
```

**Salida esperada**:
```
✓ Created repository tu-usuario/cfq-hds
Initialized empty Git repository in /home/w182/cfq_hds/cfq_hds
remote: Repository URL found at git@github.com:tu-usuario/cfq-hds.git
```

### 5.2 Opción B: Crear repositorio desde DIRECTORIO EXISTENTE ← TU CASO

Si ya tienes un proyecto con commits:

```bash
# Cambiar al directorio del proyecto
cd /home/w182/w421/cfq_hds

# Crear repositorio GitHub desde directorio actual
gh repo create cfq-hds \
  --private \
  --source=. \
  --remote=origin \
  --push \
  --description "Sistema de Hojas de Seguridad para fertilizantes Calferquim"
```

**Salida esperada**:
```
✓ Created repository tu-usuario/cfq-hds
Enumerating objects: 24, done.
Counting objects: 24, done.
Delta compression using up to 8 threads
Compressing objects: 100% (24/24), done.
Writing objects: 100% (24/24), done.
Total 24 (delta 0), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (24/24), done.
To github.com:tu-usuario/cfq-hds.git
 * [new branch]      main -> main
```

### 5.3 Verificar que se creó correctamente

```bash
gh repo view
```

**Salida esperada**:
```
name: cfq-hds
owner: tu-usuario
visibility: private
description: Sistema de Hojas de Seguridad para fertilizantes Calferquim
url: https://github.com/tu-usuario/cfq-hds
```

### 5.4 Abrir en navegador

```bash
# Abrir repositorio en el navegador
gh browse
```

---

## 6. Flujo de Trabajo Diario

### 6.1 Ciclo básico: add → commit → push

#### Agregar archivos al área de staging

```bash
# Agregar un archivo específico
git add archivo.py

# Agregar todos los archivos modificados
git add .

# Agregar archivos con patrón
git add *.py
```

#### Crear commit con mensaje claro

```bash
# Commit básico
git commit -m "Agregar scripts de generación HDS"

# Commit con mensaje estructurado (recomendado)
git commit -m "feat: agregar motor de combinación GHS para mezclas"

# Commit con descripción detallada
git commit -m "fix: resolver error en validación de pictogramas

Esta implementación corrige el problema donde se duplicaban pictogramas
cuando se combinaban más de 5 componentes en mezclas.

Closes #15"
```

**Formato de commit recomendado**:
- `feat:` para nueva funcionalidad
- `fix:` para corrección de bug
- `docs:` para documentación
- `refactor:` para reorganización de código
- `test:` para pruebas

#### Subir cambios a GitHub

```bash
# Subir la rama actual
git push origin main

# Subir rama específica
git push origin feature/generacion-pdfs
```

**Salida esperada**:
```
Enumerating objects: 5, done.
Counting objects: 5, done.
Delta compression using up to 8 threads.
Writing objects: 100% (5/5), done.
Total 5 (delta 3), reused 0 (delta 0), pack-reused 0
To github.com:tu-usuario/cfq-hds.git
   abc123d..def4567  main -> main
```

### 6.2 Ver estado y cambios

```bash
# Estado del directorio de trabajo
git status
```

**Salida esperada**:
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  modified:   scripts/generar_hds.py
```

```bash
# Ver qué cambió entre commits
git diff HEAD~1

# Comparar con remoto
git diff origin/main
```

### 6.3 Sincronizar con remoto

```bash
# Traer cambios del remoto
git pull origin main
```

**Salida esperada**:
```
Already up to date.

On branch main
Your branch is up to date with 'origin/main'.
```

```bash
# Traer sin fusionar (revisar primero)
git fetch origin

# Ver commits remotos
git log origin/main
```

### 6.4 Crear y cambiar de rama

#### Crear nueva rama

```bash
# Crear rama nueva desde la actual
git checkout -b feature/generacion-pdfs
```

**Salida esperada**:
```
Switched to a new branch 'feature/generacion-pdfs'
```

#### Cambiar a rama existente

```bash
# Cambiar a rama develop
git checkout develop

# Volver a rama anterior
git checkout -
```

#### Listar todas las ramas

```bash
# Listar ramas locales
git branch

# Listar ramas locales y remotas
git branch -a
```

**Salida esperada**:
```
  feature/generacion-pdfs
* main
  remotes/origin/develop
```

### 6.5 Fusionar ramas (merge)

#### Fusionar feature en main

```bash
# Cambiar a rama destino (main)
git checkout main

# Fusionar feature
git merge feature/generacion-pdfs
```

**Salida esperada**:
```
Updating abc1234..def5678
Fast-forward
  scripts/combinar_peligros.py | 2 +-
  scripts/utils.py                | 4 +-
 create mode 100644 output/hds/pt001.docx
```

#### Subir resultado

```bash
git push origin main
```

### 6.6 Historial de commits

```bash
# Ver últimos 10 commits en una línea
git log --oneline -10
```

**Salida esperada**:
```
abc123d (HEAD -> main) feat: agregar motor de combinación GHS
def4567 (HEAD~1) docs: actualizar plan_hds.md
ghi7890 (HEAD~2) feat: implementar estructura de directorios
jkl0123 (HEAD~3) init: commit inicial
```

```bash
# Ver con gráfico
git log --graph --oneline -10
```

**Salida esperada**:
```
* abc123d (HEAD -> main) feat: agregar motor de combinación GHS
* def4567 (HEAD~1) docs: actualizar plan_hds.md
* ghi7890 (HEAD~2) feat: implementar estructura de directorios
| * jkl0123 (HEAD~3) init: commit inicial
```

---

## 7. Git Worktrees (Trabajo en Paralelo)

### 7.1 ¿Qué son y cuándo usarlos

Un **worktree** permite tener múltiples copias del mismo repositorio en diferentes directorios, cada una en una rama diferente.

**Casos de uso**:
- Trabajar en un hotfix urgente mientras desarrollas una feature
- Revisar una rama antigua sin perder tu trabajo actual
- Tener múltiples versiones desplegadas en paralelo

### 7.2 Crear worktree para otra rama

**Escenario**: Estás en `/home/w182/w421/cfq_hds` (rama `main`) y necesitas hacer un hotfix en rama `hotfix/bug-1`.

```bash
# Crear worktree para el hotfix (se crea en directorio superior)
git worktree add ../cfq_hds-hotfix hotfix/bug-1
```

**Salida esperada**:
```
Preparing worktree (new branch 'hotfix/bug-1')
HEAD is now at abc123d
Preparing worktree (checking out branch 'hotfix/bug-1')
/path/to/cfq_hds-hotfix .git/objects
```

```bash
# Cambiar al directorio del worktree
cd ../cfq_hds-hotfix

# Trabajo en hotfix...
git commit -m "fix: resolver error crítico en validación"
git push origin hotfix/bug-1
```

### 7.3 Listar worktrees activos

```bash
git worktree list
```

**Salida esperada**:
```
/path/to/cfq_hds-hotfix            abc1234 [hotfix/bug-1]
/home/w182/w421/cfq_hds             def5678 [main]
```

### 7.4 Eliminar worktree cuando termines

```bash
# Primero asegurarte de estar FUERA del worktree
cd /home/w182/w421/cfq_hds

# Eliminar worktree
git worktree remove /path/to/cfq_hds-hotfix
```

**Salida esperada**:
```
Deleted worktree at /path/to/cfq_hds-hotfix (clean)
```

⚠️ **No elimines el directorio manualmente**: el comando también lo borra del sistema git.

### 7.5 Caso práctico desde OpenCode

Si estás trabajando en `/home/w182/w421/cfq_hds` (rama `main`):

```bash
# Necesitas crear un hotfix en rama `hotfix/bug-1`
git worktree add ../cfq_hds-hotfix hotfix/bug-1

# Cambiar al hotfix, arreglar, commitear
cd ../cfq_hds-hotfix
git commit -m "fix: resolver error urgente"
git push origin hotfix/bug-1

# Vuelve a tu trabajo original sin cambios perdidos
cd ../cfq_hds
git worktree remove ../cfq_hds-hotfix
# Ahora sigues en main donde lo dejaste
```

---

## 8. Issues desde CLI

### 8.1 Crear un issue

```bash
# Crear issue básico
gh issue create "Título del issue"

# Crear issue con cuerpo detallado (recomendado)
gh issue create "Error en combinación de pictogramas" \
  --body "### Descripción

Al generar HDS para mezclas con más de 5 componentes,
se duplican pictogramas.

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

### 8.2 Listar issues

```bash
# Ver todos los issues del repositorio
gh issue list

# Ver issues abiertos
gh issue list --state open

# Ver issues cerrados recientes
gh issue list --state closed --limit 10
```

**Salida esperada**:
```
#42  fix: Error en combinación de pictogramas  open   2 days ago
#43  docs: Actualizar README.md                  open   5 days ago
#44  feature: Agregar soporte para PDF          open   1 week ago
```

### 8.3 Ver issue específico

```bash
# Ver issue por número
gh issue view 42

# Ver issue por título
gh issue view --repo cfq-hds "Error en combinación"
```

### 8.4 Cerrar issue

```bash
# Cerrar issue con comentario
gh issue close 42 --comment "Solucionado en commit abc1234"

# Cerrar issue con referencia a commit
gh issue close --comment "Implementado en #45"
```

---

## 9. Pull Requests desde CLI

### 9.1 Crear un Pull Request

```bash
# Estás en rama feature/generacion-pdfs y quieres fusionar en main
gh pr create \
  --title "Agregar generación de PDFs" \
  --body "### Cambios

Esta PR agrega funcionalidad para convertir Markdown a PDF
directamente desde el script.

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

### 9.2 Listar Pull Requests

```bash
# Ver todas las PRs
gh pr list

# Ver PRs abiertas
gh pr list --state open

# Ver PRs específicas de un repositorio
gh pr list --repo cfq-hds
```

**Salida esperada**:
```
#15  fix: Resolver conflicto en merge            open   3 days ago
#16  feature: Agregar soporte para Etiquetas    merged  1 week ago
```

### 9.3 Ver detalles de una PR

```bash
# Ver PR por número
gh pr view 15

# Ver archivos cambiados en la PR
gh pr diff 15

# Ver estado (checks, revisiones)
gh pr checks 15
```

### 9.4 Fusionar una PR (desde CLI)

```bash
gh pr merge 15 --merge --delete-branch
```

**Salida esperada**:
```
Pull request #15 merged!
```

**Resultado**: La rama se fusiona y se borra automáticamente con `--delete-branch`.

### 9.5 Revisar cambios de una PR

```bash
# Cambiar al trabajo de la PR
gh pr checkout 15

# Volver a tu rama original
git checkout main
```

---

## 10. Comandos Útiles

### 10.1 Abrir en navegador

```bash
# Abrir repositorio actual
gh browse

# Abrir issue específico
gh browse --repo cfq-hds issues/42

# Abrir pull request
gh browse --repo cfq-hds pull/15
```

### 10.2 Crear gists (fragmentos de código rápidos)

```bash
# Desde archivo
gh gist create script.py --desc "Script de combinación GHS"

# Desde texto inline
echo "print('Hola Mundo')" | gh gist create
```

### 10.3 Crear alias (atajos)

```bash
# Crear alias para comando frecuente
gh alias set sync='git pull origin main && git push origin main'

# Usar alias
gh sync
```

### 10.4 Ver repositorio en formato web

```bash
gh repo view --web
```

### 10.5 Buscar repositorios

```bash
# Buscar por nombre
gh search cfq-hds

# Buscar por lenguaje
gh search language:python stars:>10

# Buscar por temas
gh search topics:fertilizantes
```

---

## 11. Cheatsheet (Referencia Rápida)

| Acción | Comando | Ejemplo |
|---------|---------|---------|
| **Autenticación** |
| Ver estado | `gh auth status` | Verificar autenticación |
| Login | `gh auth login` | Primera vez |
| Logout | `gh auth logout` | Cerrar sesión |
| **Repositorios** |
| Crear (vacío) | `gh repo create nombre-repo` | Nuevo proyecto |
| Crear (existente) | `gh repo create --source=. --push` | Tu caso actual |
| Clonar | `gh repo clone usuario/repo` | Copiar a local |
| Listar | `gh repo list` | Ver tus repos |
| Ver info | `gh repo view` | Detalles del repo |
| **Flujo Git** |
| Estado | `git status` | Cambios pendientes |
| Agregar | `git add archivo` | Staging |
| Commit | `git commit -m "mensaje"` | Guardar cambios |
| Subir | `git push origin main` | Sincronizar |
| Traer | `git pull origin main` | Actualizar local |
| Diferencias | `git diff` | Ver cambios |
| Branches | `git branch` | Listar ramas |
| New branch | `git checkout -b rama` | Crear rama |
| Checkout | `git checkout rama` | Cambiar rama |
| Merge | `git merge rama` | Fusionar ramas |
| Log | `git log --oneline` | Ver historial |
| **Worktrees** |
| Crear | `git worktree add ../path rama` | Hotfix paralelo |
| Listar | `git worktree list` | Ver worktrees activos |
| Eliminar | `git worktree remove path` | Limpiar worktree |
| **Issues** |
| Crear | `gh issue create "Título"` | Reportar bug |
| Listar | `gh issue list` | Ver issues |
| Ver | `gh issue view 42` | Detalles |
| Cerrar | `gh issue close 42` | Resolver issue |
| **Pull Requests** |
| Crear | `gh pr create --base main` | Proponer cambios |
| Listar | `gh pr list` | Ver PRs |
| Ver | `gh pr view 15` | Detalles |
| Merge | `gh pr merge 15` | Aprobar PR |
| **Útiles** |
| Abrir | `gh browse` | Navegador |
| Gist | `gh gist create archivo.py` | Compartir código |
| Buscar | `gh search termino` | Encontrar repos |

---

## 12. Solución de Problemas Comunes

### 12.1 Token inválido o expirado

**Error**:
```
The token in default is invalid.
- To re-authenticate, run: gh auth login -h github.com
- To forget about this account, run: gh auth logout -h github.com -u willl182
```

**Solución**:
```bash
# Cerrar sesión existente
gh auth logout

# Autenticar de nuevo
gh auth login
```

### 12.2 Permission denied (SSH)

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
# 1. Verificar llave usada por el agente
ssh-add -l

# 2. Verificar llaves existentes en ~/.ssh/
ls -la ~/.ssh/

# 3. Re-agregar llave a GitHub (si no aparece en GitHub.com/settings/keys)
gh ssh-key add ~/.ssh/id_ed25519.pub
```

### 12.3 Conflictos de merge

**Error al hacer `git pull`**:
```
CONFLICT (content): Merge conflict in archivo.py
Auto-merging; failed; Automatic merge failed; fix conflicts and then commit the result.
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

### 12.4 Worktree bloqueado

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

### 12.5 Rama ya existe en remoto

**Error al hacer `git push`**:
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
git config --global user.name "Tu Nombre Apellido"
git config --global user.email "tu-email@dominio.com"

# Configurar editor por defecto (opcional)
git config --global core.editor "code --wait"

# Configurar ramificación por defecto (main, no master)
git config --global init.defaultBranch main
```

### Verificar configuración

```bash
# Ver toda la configuración global
git config --global --list
```

---

## Recursos Adicionales

- **Documentación oficial**: https://cli.github.com/manual
- **Git Book**: https://git-scm.com/book/es/v2
- **GitHub Docs**: https://docs.github.com/es

---

**Versión de la guía**: 2.0
**Última actualización**: 2026-02-04
**Compatible con**: GitHub CLI 2.x+, Git 2.x+
