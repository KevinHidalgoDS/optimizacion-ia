# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Configuración de Rutas (Pathlib) ----------------------------------------
# Raíz del proyecto: dos niveles arriba de docs/source/
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

# Evita problemas de recursión profunda en inspecciones complejas de autodoc
sys.setrecursionlimit(5000)

# -- Información del Proyecto ------------------------------------------------
project = 'Optimización-ia'
copyright = '2026, Kevin Hidalgo'
author = 'Kevin Hidalgo'
release = '1.0.0'
version = '1.0'

# -- Configuración General ---------------------------------------------------
extensions = [
    # Extracciones automáticas de docstrings
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    # Enlaces cruzados y utilidades
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.ifconfig',
    # Tema
    'sphinx_rtd_theme',
]

# Configuración de idioma y documento raíz
language = 'es'
root_doc = 'index'
master_doc = 'index'  # Compatibilidad con versiones Sphinx < 4.0

# Archivos y carpetas a ignorar en la compilación
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**.ipynb_checkpoints',
]

templates_path = ['_templates']

# -- Configuración de Autodoc & Autosummary ---------------------------------
autosummary_generate = True
autosummary_generate_overwrite = True

# Mantiene el orden de definición original del código (no alfabético)
autodoc_member_order = 'bysource'

# Formato de type hints: 'signature', 'description' o 'none'
autodoc_typehints = 'description'

# Opciones por defecto para documentar miembros
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# (Opcional) Si en el futuro usas librerías pesadas o de nube difíciles de instalar en CI/CD:
# autodoc_mock_imports = ["azure", "pyspark"]

# -- Configuración de Napoleon (Google / NumPy Docstrings) -------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

# -- Configuración de Intersphinx --------------------------------------------
# Permite vincular tipos de datos nativos a la documentación de Python oficial
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Configuración de MathJax (LaTeX) ----------------------------------------
mathjax3_config = {
    'tex': {
        'inlineMath': [['\\(', '\\)']],
        'displayMath': [['\\[', '\\]']],
    }
}

# -- Opciones de Salida HTML -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # alabaster, sphinx_rtd_theme, groundwork
html_static_path = ['_static']

# Opciones avanzadas del tema Read the Docs
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
}
