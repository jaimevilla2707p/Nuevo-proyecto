# Kumis del Balcón — Deploy en Streamlit Cloud

## 🚀 INICIO RÁPIDO (Local)

Para ejecutar la aplicación **localmente**:

```bash
# 1. Asegúrate de estar en la carpeta del proyecto
cd /workspaces/Nuevo-proyecto

# 2. Ejecuta la aplicación
python -m streamlit run pagina-web.py
```

Esto abrirá el sitio web en `http://localhost:8501`

### Chat con la Vaquita 🐮
El chat ya funciona **sin necesidad de API key**. Prueba preguntando:
- "¿Qué tienen en el menú?"
- "¿Cuál es el precio del kumis?"
- "¿Qué me recomiendas?"
- "¿Dónde están ubicados?"

> **Nota**: Para respuestas con IA avanzada, configura una API key de OpenRouter (ver sección "Configurar la clave" abajo).

---

Instrucciones rápidas para desplegar la app en Streamlit Cloud y configurar la API key de OpenRouter.

## 1) Desplegar en Streamlit Cloud ✅
1. Ve a: https://share.streamlit.io
2. Inicia sesión con tu cuenta de **GitHub**.
3. Haz clic en **New app**.
4. Selecciona el repositorio: `jaimevilla2707p/Nuevo-proyecto`.
5. Branch: `main` (por defecto).
6. En **Main file path**, escribe: `pagina-web.py`.
7. Haz clic en **Deploy!** 🚀

> Nota: dos autorizaciones pueden aparecer: acceso al repo y autorización para ver secrets.

## 2) Configurar la clave de OpenRouter (seguridad) 🔒
- En Streamlit Cloud: entra en tu app → **Settings** → **Secrets** → añade:

```
OPENROUTER_API_KEY = "sk-..."
```

- Guarda y redeploy si es necesario.

## 3) Desarrollo local
- Para pruebas locales crea `.streamlit/secrets.toml` (NO lo subas al repo):
```
OPENROUTER_API_KEY = "sk-..."
```
- Alternativa: exporta la variable de entorno:
```
export OPENROUTER_API_KEY="sk-..."
```

## 4) Nota sobre la clave ya expuesta
He eliminado las referencias a la clave en el código y ahora la app lee la clave desde Secrets/ENV. Sin embargo, la clave puede permanecer en el historial Git. Si quieres, puedo ayudarte a eliminarla del historial con `git filter-repo` o BFG. ¿Deseas que lo haga?

---

## 5) Script para limpiar secretos y pushear (opcional)
He añadido `scripts/clean_secrets.sh`: un script interactivo que automatiza:
- Commit y push de cambios locales
- Clonado en modo espejo y uso de `git-filter-repo` para eliminar archivos o reemplazar tokens en todo el historial
- Push forzado del repo limpio al remoto (advertencia: **destructivo**, notifica a colaboradores)

Pasos rápidos:
1. Haz el script ejecutable: `chmod +x scripts/clean_secrets.sh`
2. Ejecuta: `./scripts/clean_secrets.sh` desde la raíz del repo
3. Sigue las instrucciones y confirma cada paso (el script solicita confirmaciones de seguridad)

Si quieres, ejecuto el script por ti; necesito que pegues aquí la salida de `git status --porcelain` y `git remote -v`, o me des permiso para ejecutar los comandos en este entorno. Si prefieres que lo haga remotamente en tu máquina, pega la salida y yo te indico los pasos exactos.

---

Si quieres, puedo abrir Streamlit Cloud en tu navegador para que inicies sesión y termines el despliegue. Responde "Abre Streamlit" y lo abro para ti.