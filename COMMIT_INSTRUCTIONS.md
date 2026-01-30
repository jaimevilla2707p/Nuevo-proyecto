# Instrucciones para crear el PR - feat/vaquita-deployment

## Paso 1: Crear la rama y hacer commit

Ejecuta estos comandos en la raíz del proyecto (`/workspaces/Nuevo-proyecto`):

```bash
# Crear rama
git checkout -b feat/vaquita-deployment

# Agregar todos los cambios
git add -A

# Hacer commit con el mensaje especificado
git commit -m "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube

- Añade pestaña 'Vaquita Chat' con interfaz estilo WhatsApp
- Integra OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporta consultas CRM: contactos, emails, pipeline
- Añade Dockerfile, Procfile, DEPLOYMENT.md para nube
- Workflow GitHub Actions publica imagen en GHCR
- Replaza clave real con placeholder en secrets.toml (seguridad)"

# Push a la rama remota
git push -u origin feat/vaquita-deployment
```

## Paso 2: Crear el Pull Request

### Opción A: Con GitHub CLI (recomendado)

Si tienes `gh` CLI instalado:

```bash
gh pr create \
  --title "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube" \
  --body "## Cambios principales

### ✅ Vaquita Chat
- Nueva pestaña con interfaz estilo WhatsApp
- Integración con OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporte para consultas CRM: contactos, emails, pipeline

### 🚀 Despliegue en Nube
- Dockerfile configurado para ejecutar en contenedores
- Procfile para plataformas como Heroku/Railway
- DEPLOYMENT.md con instrucciones detalladas

### 🔒 Seguridad
- Workflow GitHub Actions publica imagen en GHCR
- Clave API reemplazada con placeholder en secrets.toml
- Archivo SECURITY_NOTES.md con buenas prácticas

### 📋 Archivos incluidos
- [Dockerfile](./Dockerfile) - Imagen Docker lista para producción
- [Procfile](./Procfile) - Configuración para plataformas cloud
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía de despliegue
- [.github/workflows/publish-ghcr.yml](.github/workflows/publish-ghcr.yml) - Pipeline CI/CD
- [SECURITY_NOTES.md](./SECURITY_NOTES.md) - Prácticas de seguridad" \
  --base main \
  --head feat/vaquita-deployment
```

### Opción B: Manualmente en GitHub

Si no tienes `gh` CLI, ve a:
```
https://github.com/jaimevilla2707p/Nuevo-proyecto/compare/main...feat/vaquita-deployment
```

Y crea el PR con esta información:

**Title:**
```
feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube
```

**Body:**
```markdown
## Cambios principales

### ✅ Vaquita Chat
- Nueva pestaña con interfaz estilo WhatsApp
- Integración con OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporte para consultas CRM: contactos, emails, pipeline

### 🚀 Despliegue en Nube
- Dockerfile configurado para ejecutar en contenedores
- Procfile para plataformas como Heroku/Railway
- DEPLOYMENT.md con instrucciones detalladas

### 🔒 Seguridad
- Workflow GitHub Actions publica imagen en GHCR
- Clave API reemplazada con placeholder en secrets.toml
- Archivo SECURITY_NOTES.md con buenas prácticas

### 📋 Archivos incluidos
- [Dockerfile](./Dockerfile) - Imagen Docker lista para producción
- [Procfile](./Procfile) - Configuración para plataformas cloud
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía de despliegue
- [.github/workflows/publish-ghcr.yml](.github/workflows/publish-ghcr.yml) - Pipeline CI/CD
- [SECURITY_NOTES.md](./SECURITY_NOTES.md) - Prácticas de seguridad
```

## Estado de los archivos

Los siguientes archivos ya están en el repositorio y listos para commitear:

✅ [Dockerfile](./Dockerfile) - Configurado para Python 3.11 + Streamlit
✅ [Procfile](./Procfile) - Para despliegue en Heroku/Railway
✅ [DEPLOYMENT.md](./DEPLOYMENT.md) - Instrucciones de despliegue detalladas
✅ [.github/workflows/publish-ghcr.yml](.github/workflows/publish-ghcr.yml) - Pipeline CI/CD
✅ [SECURITY_NOTES.md](./SECURITY_NOTES.md) - Guía de seguridad
✅ [requirements.txt](./requirements.txt) - Dependencias actualizadas
✅ [README.md](./README.md) - Documentación principal

## Validación

Verifica que todo está en orden:

```bash
# Ver estado
git status

# Ver cambios pendientes
git diff --cached

# Ver rama actual
git branch -a
```

---

**Nota**: Una vez que completes el paso 1 y 2, el PR será visible en GitHub automáticamente.
