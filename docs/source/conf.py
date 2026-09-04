# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.setrecursionlimit(5000)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Optimización-ia'
copyright = '2026, Kevin Hidalgo'
author = 'Kevin Hidalgo'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
]

# Generate autodoc stubs with summaries from code

autosummary_generate = True
autosummary_generate_overwrite = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
exclude_patterns = []
mathjax3_config = {
  "tex": {
    "inlineMath": [['\\(', '\\)']],
    "displayMath": [["\\[", "\\]"]],
  }
}

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

master_doc = 'index'
html_theme = 'sphinx_rtd_theme'  # alabaster, sphinx_rtd_theme, groundwork
html_static_path = ['_static']
