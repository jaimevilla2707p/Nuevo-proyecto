#!/bin/bash
cd /workspaces/Nuevo-proyecto
pkill -f "streamlit run" || true
sleep 2
/workspaces/Nuevo-proyecto/.venv/bin/python -m streamlit run pagina-web.py --server.headless true --logger.level=error
