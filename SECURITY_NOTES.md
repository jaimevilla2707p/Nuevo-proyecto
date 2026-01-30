Seguridad y buenas prácticas

- No incluyas claves API en el código.
- Usa `st.secrets` en Streamlit Cloud o variables de entorno.
- Añade `.streamlit/secrets.toml` a `.gitignore` (ya lo hice).

Para eliminar claves comprometidas del historial Git, usa `git filter-repo` o BFG:

Ejemplo con git filter-repo (requiere instalación):

```
git clone --mirror git@github.com:jaimevilla2707p/Nuevo-proyecto.git
cd Nuevo-proyecto.git
git filter-repo --replace-refs delete-no-add --invert-paths --paths .streamlit/secrets.toml
# O usar --path-glob para filtrar por archivo específico
# Luego empuja los cambios forzando el repo remoto (¡cuidado!):
git push --force
```

Si quieres, realizo este proceso por ti tras tu confirmación.