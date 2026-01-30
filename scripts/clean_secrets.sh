#!/usr/bin/env bash
set -euo pipefail

# clean_secrets.sh — Safe helper to commit, push and optionally remove secrets from git history
# Usage: run from the repository root: ./scripts/clean_secrets.sh

REPO_ROOT=$(pwd)

echo "-- Inicio: script para commitear, pushear y limpiar secretos del historial --"

# Ensure we're in a git repository
if ! command -v git >/dev/null 2>&1; then
  echo "Error: git no está instalado. Instálalo y vuelve a intentarlo." >&2
  exit 1
fi

if [ ! -d ".git" ]; then
  echo "No parece ser la raíz de un repo Git. Ve a la carpeta del proyecto y vuelve a ejecutar." >&2
  exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Advertencia: estás en la rama '$CURRENT_BRANCH'. Recomiendo usar 'main' para este flujo." 
  read -p "¿Deseas continuar? (si/no): " cont
  if [ "$cont" != "si" ]; then
    echo "Abortando."; exit 1
  fi
fi

# Show git status
echo "Estado de git (por favor revisa):"
git status --short

read -p "¿Deseas añadir y commitear todos los cambios actuales? (si/no): " do_commit
if [ "$do_commit" = "si" ]; then
  read -p "Mensaje de commit (default: feat: limpiar secretos y preparar deploy): " msg
  msg=${msg:-"feat: limpiar secretos y preparar deploy"}
  git add -A
  git commit -m "$msg"
  echo "Commit creado." 
else
  echo "No se creó commit. Asegúrate de tener los cambios comiteados antes de purgar el historial." 
fi

read -p "¿Deseas hacer push a 'origin main' ahora? (si/no): " do_push
if [ "$do_push" = "si" ]; then
  git push origin main
  echo "Push completado." 
else
  echo "No se hizo push. Recuerda pushear antes de purgar el historial para que el mirror tenga la referencia correcta." 
fi

read -p "¿Deseas purgar secretos del historial con git-filter-repo? (recomendado pero destructivo) (si/no): " do_purge
if [ "$do_purge" != "si" ]; then
  echo "Proceso finalizado sin reescribir historial. Recuerda añadir la clave nueva a Streamlit Secrets si aún no lo hiciste."
  exit 0
fi

# Check git-filter-repo
if ! python -c "import importlib.util,sys;print(importlib.util.find_spec('git_filter_repo') is not None)" 2>/dev/null | grep -q True; then
  echo "git-filter-repo no parece instalado en este entorno Python. Se puede instalar con: pip install git-filter-repo"
  read -p "¿Deseas instalarlo ahora con pip? (si/no): " install_gr
  if [ "$install_gr" = "si" ]; then
    pip install git-filter-repo
  else
    echo "Instala git-filter-repo e intenta de nuevo."; exit 1
  fi
fi

REMOTE_URL=$(git config --get remote.origin.url)
if [ -z "$REMOTE_URL" ]; then
  echo "No se encontró remote.origin.url. Configura el remote y vuelve a intentar."; exit 1
fi

TMPDIR=$(mktemp -d)
echo "Clonando espejo del repo en: $TMPDIR"
git clone --mirror "$REMOTE_URL" "$TMPDIR/repo.git"
pushd "$TMPDIR/repo.git" >/dev/null

echo "Métodos disponibles para purgar secretos:
  1) Eliminar archivo (por ejemplo: .streamlit/secrets.toml)
  2) Reemplazar token específico por [REDACTED]"
read -p "Selecciona método (1/2): " method

if [ "$method" = "1" ]; then
  read -p "Introduce la ruta relativa del archivo a eliminar (por ejemplo .streamlit/secrets.toml): " path_to_remove
  if [ -z "$path_to_remove" ]; then
    echo "Ruta vacía. Abortando."; exit 1
  fi
  echo "Ejecutando: git filter-repo --path $path_to_remove --invert-paths"
  git filter-repo --path "$path_to_remove" --invert-paths
  echo "Archivo eliminado del historial." 

elif [ "$method" = "2" ]; then
  echo "ADVERTENCIA: vas a reemplazar una cadena en todo el historial (ej. una clave API)."
  read -p "Introduce exactamente la cadena secreta a reemplazar (se mostrará en pantalla mientras escribes): " secret
  if [ -z "$secret" ]; then
    echo "Cadena vacía. Abortando."; exit 1
  fi
  printf '%s==%s
' "$secret" "[REDACTED]" > my_replacements.txt
  echo "Ejecutando: git filter-repo --replace-text my_replacements.txt"
  git filter-repo --replace-text my_replacements.txt
  echo "Reemplazo realizado." 
else
  echo "Opción inválida. Abortando."; exit 1
fi

read -p "Se va a forzar el push del repo limpio al remoto (esto reescribe el historial remoto). Escribe 'FORCE' para confirmar: " confirm
if [ "$confirm" != "FORCE" ]; then
  echo "Confirmación no recibida. No se hará push. Los cambios están en: $TMPDIR/repo.git"; popd >/dev/null; exit 0
fi

# Push forzado
git push --force
echo "Push forzado completo. El historial remoto ha sido reescrito."

popd >/dev/null

echo "Limpieza completada. NOTAS:
 - Revoca/regenera cualquier clave comprometida en el proveedor (p.ej. OpenRouter).
 - Añade la nueva clave en Streamlit Cloud (Settings → Secrets → OPENROUTER_API_KEY).
 - Informa a los colaboradores que deben re-clonar el repo." 

echo "Directorio mirror con resultado: $TMPDIR/repo.git (se puede borrar cuando confirmes que todo está bien)."

echo "-- FIN --" 
