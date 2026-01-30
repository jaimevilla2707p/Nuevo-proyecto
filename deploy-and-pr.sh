#!/bin/bash
# Script para hacer commit, push y abrir PR de todos los cambios
# Ejecución: bash deploy-and-pr.sh

set -e

echo "🚀 Iniciando deploy y PR automation..."

# 1. Crear rama
echo "📌 Creando rama feat/vaquita-deployment..."
git checkout -b feat/vaquita-deployment

# 2. Añadir todos los cambios
echo "📦 Añadiendo cambios..."
git add -A

# 3. Crear commit
echo "💾 Creando commit..."
git commit -m "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube

- Añade pestaña 'Vaquita Chat' con interfaz estilo WhatsApp
- Integra OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporta consultas CRM: contactos, emails, pipeline
- Añade Dockerfile, Procfile, DEPLOYMENT.md para nube
- Workflow GitHub Actions publica imagen en GHCR
- Replaza clave real con placeholder en secrets.toml (seguridad)

Instrucciones de despliegue en DEPLOYMENT.md"

# 4. Pushear rama
echo "🔼 Pusheando rama..."
git push -u origin feat/vaquita-deployment

# 5. Crear PR (requiere GitHub CLI)
if command -v gh &> /dev/null; then
    echo "📝 Creando PR..."
    gh pr create \
      --title "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube" \
      --body "## Resumen

✨ Añade funcionalidad completa de chat con IA y prepara despliegue automático en nube.

### Cambios principales

1. **Vaquita Chat (WhatsApp-style)**
   - Nueva pestaña en AI Assistant con interfaz tipo WhatsApp
   - Área de chat con altura fija y scroll
   - Burbujas de usuario/bot diferenciadas

2. **IA mejorada**
   - Integra OpenRouter API cuando está disponible
   - Fallback local inteligente que responde preguntas sobre Sevilla (Valle del Cauca)
   - Responde a intents: contactos, emails, pipeline, cálculos
   - System prompt en español

3. **Despliegue en nube**
   - \`Dockerfile\`: imagen Python 3.11 slim
   - \`Procfile\`: para Heroku/Railway
   - \`DEPLOYMENT.md\`: guía paso a paso
   - Workflow GitHub Actions: publica imagen en GHCR

4. **Seguridad**
   - Clave reemplazada con placeholder en \`.streamlit/secrets.toml\`
   - Instrucciones para usar secrets del proveedor

### Cómo probar
\`\`\`bash
python -m pip install -r requirements.txt
export OPENROUTER_API_KEY=\"tu_clave\"
streamlit run crm_app.py
\`\`\`

### Próximos pasos
1. Merge a \`main\`
2. GitHub Actions publica imagen en GHCR
3. Despliega en Render/Heroku/Streamlit Cloud
4. Configura \`OPENROUTER_API_KEY\` como secret

Ver \`DEPLOYMENT.md\` para instrucciones detalladas." \
      --base main \
      --head feat/vaquita-deployment
    echo "✅ PR creado exitosamente."
else
    echo "⚠️  GitHub CLI (gh) no está instalado. Crea el PR manualmente en GitHub:"
    echo "   https://github.com/$GITHUB_REPOSITORY/compare/main...feat/vaquita-deployment"
fi

echo "🎉 ¡Deploy y PR completados!"
