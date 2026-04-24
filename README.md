# Python
venv/
__pycache__/
*.py[cod]
*.pyo
.Python

# Variables de entorno
.env

# Flask-Migrate (solo ignorar el cache, no las migraciones)
migrations/versions/__pycache__/

# Base de datos
*.db
*.sqlite3

# Tailwind / Node
node_modules/
package-lock.json

# CSS compilado (se genera con npm run build)
app/static/css/output.css

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db