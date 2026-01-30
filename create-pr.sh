#!/bin/bash

# Script para crear el PR feat/vaquita-deployment
# Uso: bash create-pr.sh

set -e

PROJECT_DIR="/workspaces/Nuevo-proyecto"
cd "$PROJECT_DIR" || exit 1

echo "🚀 Iniciando proceso de creación de PR..."
echo ""

# Paso 1: Crear rama
echo "📌 Paso 1: Crear rama feat/vaquita-deployment"
if git rev-parse --verify feat/vaquita-deployment > /dev/null 2>&1; then
    echo "⚠️  La rama ya existe. Usando rama existente..."
    git checkout feat/vaquita-deployment
else
    git checkout -b feat/vaquita-deployment
    echo "✅ Rama creada"
fi
echo ""

# Paso 2: Agregar cambios
echo "📌 Paso 2: Agregando cambios"
git add -A
echo "✅ Cambios agregados"
echo ""

# Paso 3: Verificar cambios pendientes
echo "📌 Paso 3: Cambios pendientes de commit:"
git diff --cached --stat
echo ""

# Paso 4: Hacer commit
echo "📌 Paso 4: Creando commit"
git commit -m "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube

- Añade pestaña 'Vaquita Chat' con interfaz estilo WhatsApp
- Integra OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporta consultas CRM: contactos, emails, pipeline
- Añade Dockerfile, Procfile, DEPLOYMENT.md para nube
- Workflow GitHub Actions publica imagen en GHCR
- Replaza clave real con placeholder en secrets.toml (seguridad)" || echo "⚠️  No hay cambios para commitear"
echo "✅ Commit creado"
echo ""

# Paso 5: Push a la rama remota
echo "📌 Paso 5: Haciendo push a origin"
git push -u origin feat/vaquita-deployment
echo "✅ Push completado"
echo ""

# Paso 6: Crear PR con gh si está disponible
echo "📌 Paso 6: Crear Pull Request"
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI detectado. Creando PR..."
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
- Dockerfile - Imagen Docker lista para producción
- Procfile - Configuración para plataformas cloud
- DEPLOYMENT.md - Guía de despliegue
- .github/workflows/publish-ghcr.yml - Pipeline CI/CD
- SECURITY_NOTES.md - Prácticas de seguridad" \
      --base main \
      --head feat/vaquita-deployment
    
    PR_URL=$(gh pr view --json url --jq .url 2>/dev/null || echo "")
    if [ -n "$PR_URL" ]; then
        echo "✅ PR Creado: $PR_URL"
    fi
else
    echo "⚠️  GitHub CLI no disponible. Crear PR manualmente en:"
    echo "   https://github.com/jaimevilla2707p/Nuevo-proyecto/compare/main...feat/vaquita-deployment"
fi
echo ""

echo "✨ Proceso completado!"
echo ""
echo "Resumen:"
echo "  • Rama: feat/vaquita-deployment"
echo "  • Commit: feat: integrar Vaquita chat, IA con datos de Sevilla..."
echo "  • Destino: https://github.com/jaimevilla2707p/Nuevo-proyecto"
echo ""
