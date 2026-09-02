#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""config
Configuraciones generales del laboratorio.

Proyecto: optimizacion-ia

Tema: Configuraciones variables generales

Programa: config.py

Soporte: kfhidalgoh@unal.edu.co

version: 1.0.0

lenguaje: Python 3.14.5

CD: 20260902

LUD: 20260902

Comentarios:
    - 2026-09-02 Kevin Hidalgo -> creación.
"""

__authors__ = ["Kevin Hidalgo"]
__contact__ = "kfhidalgoh@unal.edu.co"
__copyright__ = "Copyright 2026, Universidad Nacional de Colombia"
__credits__ = ["Kevin Hidalgo"]
__email__ = "kfhidalgoh@unal.edu.co"
__status__ = "Desarrollo"
__version__ = "1.0.0"
__date__ = "2026-09-02"

import os
import sys
from pathlib import Path
from time import localtime, strftime

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class PathsData(BaseModel):
    raw: str
    interim: str
    processed: str
    external: str

class PathsModels(BaseModel):
    trained: str

class PathsReports(BaseModel):
    figures: str

class Paths(BaseModel):
    data: PathsData
    models: PathsModels
    reports: PathsReports

class Config(BaseModel):
    project: dict
    paths: Paths


def load_config(path: str = "config/config.yaml") -> Config:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    except FileNotFoundError:
        ruta_config = Path(__file__).resolve().parent / "config.yaml"
        with ruta_config.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    return Config(**raw)

# -----------------------------------------------------------------------------
# DIRECTORIOS LOCALES
# -----------------------------------------------------------------------------

PROJECT_PATH = Path(__file__).resolve().parent
LOG_DIRECTORY = (
    PROJECT_PATH / "logs"
)

# -----------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

LOG_FORMAT = (
    "%(asctime)s "
    "[%(levelname)s] "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# -----------------------------------------------------------------------------
# ARCHIVOS
# -----------------------------------------------------------------------------

def get_main_name() -> str:
    """
    Obtiene el nombre del archivo o notebook principal en ejecución.

    La función determina el contexto de ejecución (terminal, Jupyter, IPython)
    y devuelve el nombre base del archivo o notebook.

    Returns:
        str: Nombre del archivo o notebook principal sin extensión.
    """
    main_file = _get_main_file_path()

    if main_file:
        return _extract_name_from_file(main_file)

    return _get_fallback_name()


def _get_main_file_path() -> Path | None:
    """
    Obtiene la ruta del archivo principal en ejecución.

    Returns:
        Optional[Path]: Ruta del archivo principal o None si no se puede determinar.
    """
    main_module = sys.modules.get('__main__')
    if not main_module:
        return None

    main_file = getattr(main_module, '__file__', None)
    if not main_file:
        return None

    return Path(main_file)


def _extract_name_from_file(file_path: Path) -> str:
    """
    Extrae el nombre base del archivo según el contexto de ejecución.

    Args:
        file_path: Ruta del archivo principal.

    Returns:
        str: Nombre base del archivo o notebook.
    """
    file_str = str(file_path)

    if _is_terminal_execution(file_str):
        return file_path.stem

    notebook_name = _get_notebook_name()
    if notebook_name:
        return notebook_name

    return file_path.stem


def _is_terminal_execution(file_path_str: str) -> bool:
    """
    Determina si la ejecución es desde terminal (no Jupyter/IPython).

    Args:
        file_path_str: Ruta del archivo como cadena.

    Returns:
        bool: True si es ejecución desde terminal, False en caso contrario.
    """
    return 'ipykernel' not in file_path_str and 'ipython' not in file_path_str


def _get_notebook_name() -> str | None:
    """
    Intenta obtener el nombre del notebook en entorno Jupyter/IPython.

    Returns:
        Optional[str]: Nombre del notebook o None si no se puede obtener.
    """
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        if not ipython or not hasattr(ipython, 'config'):
            return None

        connection_file = ipython.config.get('IPKernelApp', {}).get(
            'connection_file', ''
        )
        if not connection_file:
            return None

        return _clean_notebook_name(connection_file)

    except (ImportError, AttributeError):
        return None


def _clean_notebook_name(connection_file_path: str) -> str:
    """
    Limpia y formatea el nombre del notebook desde la ruta de conexión.

    Args:
        connection_file_path: Ruta del archivo de conexión del kernel.

    Returns:
        str: Nombre del notebook limpio y formateado.
    """
    raw_name = Path(connection_file_path).stem
    # Eliminar prefijo 'kernel-' y reemplazar guiones por guiones bajos
    clean_name = raw_name.replace('kernel-', '').replace('-', '_')
    return clean_name


def _get_fallback_name() -> str:
    """
    Obtiene un nombre alternativo cuando no se puede determinar el principal.

    Intenta obtener información del entorno interactivo o usa el nombre
    del script actual como último recurso.

    Returns:
        str: Nombre alternativo para el contexto actual.
    """
    fallback_name = _get_interactive_kernel_name()
    if fallback_name:
        return fallback_name

    return Path(__file__).stem


def _get_interactive_kernel_name() -> str | None:
    """
    Obtiene el nombre del kernel en entorno interactivo (Jupyter/IPython).

    Returns:
        Optional[str]: Nombre del kernel o None si no es un entorno interactivo.
    """
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        if not ipython:
            return None

        connection_file = ipython.config.get('IPKernelApp', {}).get(
            'connection_file', ''
        )
        if not connection_file:
            return None

        # Formatear nombre del notebook desde kernel
        raw_name = Path(connection_file).stem.replace('kernel-', '')
        return f"notebook_{raw_name}"

    except (ImportError, AttributeError):
        return None

main_name = get_main_name()
LOG_FILE = LOG_DIRECTORY / (
    f"{strftime('%Y%m%d%H%M%S', localtime())}_{main_name}.log"
)
