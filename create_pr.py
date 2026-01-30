#!/usr/bin/env python3
"""
Script para crear automáticamente el PR feat/vaquita-deployment
Ejecutar: python3 create_pr.py
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Ejecutar comando y reportar resultado"""
    print(f"\n📌 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/workspaces/Nuevo-proyecto")
        if result.returncode == 0:
            print(f"✅ Éxito")
            if result.stdout:
                print(result.stdout[:500])  # Mostrar primeros 500 chars
            return True
        else:
            print(f"⚠️  Aviso: {result.stderr[:300]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 Iniciando proceso de creación de PR...")
    print("=" * 60)
    
    os.chdir("/workspaces/Nuevo-proyecto")
    
    # Paso 1: Verificar que estamos en un repo git
    print("\n📋 Verificando repositorio git...")
    result = subprocess.run("git status", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ No estamos en un repositorio git")
        sys.exit(1)
    print("✅ Repositorio git detectado")
    
    # Paso 2: Verificar rama main existe
    result = subprocess.run("git branch -a | grep main", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️  Rama 'main' no encontrada, intentando 'master'...")
    
    # Paso 3: Crear rama
    run_command(
        "git checkout -b feat/vaquita-deployment 2>/dev/null || git checkout feat/vaquita-deployment",
        "Paso 1: Crear o cambiar a rama feat/vaquita-deployment"
    )
    
    # Paso 4: Agregar cambios
    run_command("git add -A", "Paso 2: Agregar todos los cambios")
    
    # Paso 5: Ver lo que se va a commitear
    print("\n📋 Cambios que se van a commitear:")
    result = subprocess.run("git diff --cached --stat", shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    # Paso 6: Hacer commit
    run_command(
        """git commit -m "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube

- Añade pestaña 'Vaquita Chat' con interfaz estilo WhatsApp
- Integra OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporta consultas CRM: contactos, emails, pipeline
- Añade Dockerfile, Procfile, DEPLOYMENT.md para nube
- Workflow GitHub Actions publica imagen en GHCR
- Replaza clave real con placeholder en secrets.toml (seguridad)\"""",
        "Paso 3: Crear commit"
    )
    
    # Paso 7: Push
    run_command("git push -u origin feat/vaquita-deployment", "Paso 4: Hacer push a GitHub")
    
    # Paso 8: Mostrar URL para crear PR
    print("\n" + "=" * 60)
    print("\n✅ ¡Proceso completado!")
    print("\n📋 Próximos pasos:")
    print("=" * 60)
    print("\n1️⃣  Si tienes GitHub CLI (gh):")
    print("""
   gh pr create \\
     --title "feat: integrar Vaquita chat, IA con datos de Sevilla, y preparar despliegue en nube" \\
     --body "## ✅ Vaquita Chat
- Nueva pestaña con interfaz estilo WhatsApp
- Integración con OpenRouter API para respuestas inteligentes
- Fallback local con datos históricos de Sevilla (Valle del Cauca)
- Soporte para consultas CRM: contactos, emails, pipeline

## 🚀 Despliegue en Nube
- Dockerfile configurado para ejecutar en contenedores
- Procfile para plataformas como Heroku/Railway
- DEPLOYMENT.md con instrucciones detalladas

## 🔒 Seguridad
- Workflow GitHub Actions publica imagen en GHCR
- Clave API reemplazada con placeholder en secrets.toml
- Archivo SECURITY_NOTES.md con buenas prácticas" \\
     --base main \\
     --head feat/vaquita-deployment
    """)
    
    print("\n2️⃣  Si no tienes GitHub CLI, abre esta URL:")
    print("   https://github.com/jaimevilla2707p/Nuevo-proyecto/compare/main...feat/vaquita-deployment")
    print("\n" + "=" * 60)
    
    # Mostrar información de la rama
    print("\n📊 Información de la rama:")
    subprocess.run("git log --oneline -3", shell=True)
    subprocess.run("git branch -vv", shell=True)

if __name__ == "__main__":
    main()
