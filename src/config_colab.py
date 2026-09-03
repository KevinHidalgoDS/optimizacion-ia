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

import hashlib
import logging
import os
import sys
import uuid
from pathlib import Path
from time import localtime, strftime

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# ============================================================================
# Modelos de datos para validación
# ============================================================================
class ProjectConfig(BaseModel):
    """Información general del proyecto."""
    name: str = Field(..., description="Nombre del proyecto")
    version: str = Field(..., description="Version del proyecto")
    description: str = Field(..., description="Descripcion del proyecto")
    author: str = Field(..., description="Autor del proyecto")
    email: str = Field(..., description="Correo del autor del proyecto")


class PathsData(BaseModel):
    """Configuración de rutas para datos."""
    raw: str = Field(..., description="Ruta para datos crudos")
    interim: str = Field(..., description="Ruta para datos intermedios")
    processed: str = Field(..., description="Ruta para datos procesados")
    external: str = Field(..., description="Ruta para datos externos")


class PathsModels(BaseModel):
    """Configuración de rutas para modelos."""
    trained: str = Field(..., description="Ruta para modelos entrenados")


class PathsReports(BaseModel):
    """Configuración de rutas para reportes."""
    figures: str = Field(..., description="Ruta para figuras")


class Paths(BaseModel):
    """Configuración completa de rutas del proyecto."""
    data: PathsData = Field(..., description="Rutas de datos")
    models: PathsModels = Field(..., description="Rutas de modelos")
    reports: PathsReports = Field(..., description="Rutas de reportes")


class EnvironmentConfig(BaseModel):
    """Configuración del entorno de ejecución."""
    nombre: str = Field(..., description="Nombre del proyecto")
    entorno: str = Field(..., description="Entorno de ejecución (local/colab)")
    ide: str = Field(..., description="IDE utilizado")


class LoggingConfig(BaseModel):
    """Configuración del sistema de logging."""
    level: str = Field("INFO", description="Nivel de logging")
    format: str = Field("%(asctime)s [%(levelname)s] %(message)s", description="Formato de logging")
    date_format: str = Field("%Y-%m-%d %H:%M:%S", description="Formato de fecha")
    dir: str = Field("logs", description="Directorio de logs")

class Config(BaseModel):
    """Configuración completa del proyecto."""
    project: ProjectConfig = Field(..., description="Información general del proyecto")
    paths: Paths = Field(..., description="Rutas del proyecto")
    environment: EnvironmentConfig = Field(..., description="Entorno")
    logging: LoggingConfig = Field(..., description="Configuración de logging")


class EnvironmentManager:
    """Gestor principal para el entorno de ejecución y configuraciones.

    Se encarga de detectar si el código se ejecuta en Google Colab o
    localmente, y ajusta el directorio raíz del proyecto consecuentemente.
    """

    def __init__(self, project_name: str = "optimizacion-ia"):
        """Inicializa el gestor y carga las configuraciones.

        Args:
            project_name (str): Nombre del proyecto para armar la ruta en Drive.
        """
        self.project_name = project_name
        self.is_colab = self._detect_colab()
        self.base_path = self._set_base_path()
        self.config = self._load_yaml()

    def _detect_colab(self) -> bool:
        """Verifica si el módulo 'google.colab' está en el sistema.

        Returns:
            bool: True si está en Colab, False en local.
        """
        return 'google.colab' in sys.modules

    def _set_base_path(self) -> Path:
        """Define la ruta base del proyecto según el entorno detectado.

        Returns:
            Path: Ruta absoluta a la raíz del proyecto.
        """
        if self.is_colab:
            # Ruta en Drive
            return Path(f"/content/drive/MyDrive/MaestriaIngAnalitica/{self.project_name}")
        else:
            # Asume que este archivo está en src/, un nivel abajo de la raíz
            return Path(__file__).resolve().parent.parent

    def _load_yaml(self) -> Config:
        """Carga el archivo config.yaml y valida su estructura.

        Returns:
            Config: Objeto validado con los parámetros del YAML.

        Raises:
            FileNotFoundError: Si no se encuentra el archivo de configuración.
        """
        config_path = self.base_path / "config" / "config.colab.yaml"
        logging.debug("config_path: %s", config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {config_path}")

        with config_path.open("r", encoding="utf-8") as file:
            raw_config = yaml.safe_load(file)

        return Config(**raw_config)

    def get_path(self, relative_path: str) -> Path:
        """Convierte una ruta relativa del YAML a una ruta absoluta del sistema.

        Args:
            relative_path (str): Ruta extraída del objeto Config.

        Returns:
            Path: Ruta absoluta lista para usar.
        """
        return self.base_path / relative_path


def _get_colab_hash():
    """Genera un hash corto y único para la sesión actual del kernel."""
    session_id = f"{os.getpid()}-{uuid.uuid4()}"
    return hashlib.md5(session_id.encode()).hexdigest()[:8]


def setup_dynamic_logger(env_manager, name=None):
    """Configura el logger generando el nombre del archivo dinámicamente."""
    cfg = env_manager.config.logging

    # 1. Simular __file__ en Colab obteniendo el nombre del kernel/notebook
    file_name = "colab_notebook"
    try:
        from IPython import get_ipython

        ipy = get_ipython()
        if ipy and hasattr(ipy, "config"):
            conn_file = ipy.config.get("IPKernelApp", {}).get("connection_file", "")
            if conn_file:
                # Limpia el nombre del archivo de conexión del kernel
                file_name = Path(conn_file).stem.replace("kernel-", "").replace("-", "_")
                logging.debug("File name: %s", file_name)
    except Exception:
        pass  # Si falla (ej. en terminal local), usará 'colab_notebook'

    # Si estamos en un script .py local, sí podríamos usar sys.argv[0] o __file__
    import sys

    if not "ipykernel" in sys.modules and len(sys.argv) > 0:
        file_name = Path(sys.argv[0]).stem

    # 2. Generar el nombre del log: YYYYMMDDHHMMSS_{file_name}.log
    timestamp = strftime("%Y%m%d%H%M%S", localtime())
    if file_name != "colab_notebook":
        log_filename = f"{timestamp}_{file_name}.log"
    else:
        file_name = name if name else _get_colab_hash()
        log_filename = f"{timestamp}_{file_name}.log"
    # 3. Crear directorio y definir ruta completa
    log_dir = env_manager.get_path(cfg.dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_filename

    # 4. Configurar el Logger
    logger = logging.getLogger("OptimizacionIA")
    logger.setLevel(getattr(logging, cfg.level))

    # Limpiar handlers previos si la celda se ejecuta múltiples veces
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(fmt=cfg.format, datefmt=cfg.date_format)

    # Handler Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler Archivo
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger, log_path
