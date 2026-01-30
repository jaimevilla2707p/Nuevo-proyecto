# Despliegue (Deployment)

Opciones para desplegar la app Streamlit públicamente.

1) Render (recomendado por simplicidad)
- Crear cuenta en https://render.com
- Nuevo "Web Service" → conectar al repo de GitHub
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run crm_app.py --server.port $PORT --server.address 0.0.0.0`
- Expose port: Render usa `$PORT` automáticamente.
- Añadir secret `OPENROUTER_API_KEY` en Environment > Environment Variables.

2) Streamlit Community Cloud (fácil para proyectos públicos)
- Empuja tu repo a GitHub
- En https://share.streamlit.io crea una nueva app apuntando a tu repo y rama
- En Settings > Secrets añade `OPENROUTER_API_KEY` (no subir clave al repo)

3) Railway / Heroku
- Railway: crear nuevo proyecto, conectar repo, usar Dockerfile o build command `pip install -r requirements.txt` y start command como arriba.
- Heroku: crear app, subir repo o usar GitHub integration. Asegúrate de definir `PORT` y `OPENROUTER_API_KEY` en Config Vars. Usa `Procfile` incluido.

4) Docker (genérico)
- Construir imagen:
  ```bash
  docker build -t nuevo-proyecto:latest .
  docker run -p 8501:8501 -e OPENROUTER_API_KEY="$OPENROUTER_API_KEY" nuevo-proyecto:latest
  ```

Secrets / API keys
- NUNCA comitees claves en el repositorio público. Usa los mecanismos de secretos del proveedor (Render/Streamlit/Heroku/GitHub Actions).
- En desarrollo local puedes usar `./.streamlit/secrets.toml` (ya existe en el repo) o exportar `OPENROUTER_API_KEY`.

Comandos útiles (resumen):
```bash
# Build and test locally with Docker
docker build -t nuevo-proyecto:latest .
docker run -p 8501:8501 -e OPENROUTER_API_KEY="$OPENROUTER_API_KEY" nuevo-proyecto:latest

# Or run directly
pip install -r requirements.txt
streamlit run crm_app.py
```

Si quieres, puedo generar automáticamente el PR con estos archivos (necesito que ejecutes los comandos git en tu entorno) o puedo preparar un workflow de GitHub Actions para desplegar automáticamente en Render.
