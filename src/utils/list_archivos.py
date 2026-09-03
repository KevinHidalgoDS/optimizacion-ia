# %%
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Este código proporciona una implementación robusta y lista para producción para realizar
solicitudes POST en Python.

Ejemplo completo de cliente HTTP para solicitudes POST con la biblioteca requests.
Este módulo proporciona implementaciones robustas y listas para producción
para realizar solicitudes POST a APIs RESTful.

Programa: no_post_semestre_process.py

Soporte: kevin.hidalgo@globalmvm.com

Versión: 1.0.0

Lenguaje: Python 3.11.9

CD: 20251222

LUD: 20260723

Comentarios:
    * 2025-12-22 Kevin Hidalgo -> creación.
"""

__authors__ = ["Kevin Hidalgo"]
__contact__ = "kevin.hidalgo@globalmvm.com"
__copyright__ = "Copyright 2025, MVM ingenieria de software"
__credits__ = ["Kevin Hidalgo"]
__email__ = "kevin.hidalgo@globalmvm.com"
__status__ = "Desarrollo"
__version__ = "1.0.0"
__date__ = "2025-12-22"

import logging
import tempfile
from datetime import datetime
from pathlib import Path

from src.utils import logger as log

logger = log.LOGGER

def generar_rutas_garantias(ruta_carpeta: str | Path) -> str:
    """
    Genera una cadena de rutas relativas formateadas para los archivos de una carpeta.

    La función lee el contenido de la carpeta especificada, filtra únicamente los
    archivos (ignorando subcarpetas) y construye una ruta destino basada en la
    fecha actual del sistema operativo.

    El formato de salida para cada archivo es:
    garantias-bankgar/Semestre/YYYY/MM/YYYYMMDD/nombre_archivo.extension

    Args:
        ruta_carpeta (Union[str, Path]): La ruta absoluta o relativa de la carpeta
            origen a procesar.

    Returns:
        str: Una cadena de texto con las rutas relativas generadas, separadas
            exclusivamente por comas (,). Retorna una cadena vacía si la carpeta
            existe pero no contiene archivos.

    Raises:
        FileNotFoundError: Si la ruta especificada no existe en el sistema.
        NotADirectoryError: Si la ruta existe pero corresponde a un archivo en
            lugar de un directorio.
        PermissionError: Si no se tienen los permisos necesarios para leer el
            contenido del directorio.
    """
    # Convertimos la entrada a un objeto Path por seguridad y conveniencia
    directorio = Path(ruta_carpeta)

    # Validación de existencia
    if not directorio.exists():
        raise FileNotFoundError(f"La ruta origen no existe: {directorio}")

    # Validación de tipo (debe ser carpeta, no archivo)
    if not directorio.is_dir():
        raise NotADirectoryError(
            f"La ruta especificada no es un directorio válido: {directorio}"
        )

    # Obtener solo los archivos del directorio principal (sin recursividad)
    archivos = [archivo for archivo in directorio.iterdir() if archivo.is_file()]

    # Manejo de carpeta vacía
    if not archivos:
        return ""

    # Construcción de las variables de fecha actuales
    fecha_actual = datetime.now()
    yyyy = fecha_actual.strftime("%Y")
    mm = fecha_actual.strftime("%m")
    yyyymmdd = fecha_actual.strftime("%Y%m%d")

    # Prefijo base para todas las rutas
    prefijo_ruta = f"garantias-bankgar/Semestre/{yyyy}/{mm}/{yyyymmdd}"

    # Generación de la lista de rutas finales
    rutas_formateadas = [f"{prefijo_ruta}/{archivo.name}" for archivo in archivos]

    # Retorno de la cadena unida por comas
    return ",".join(rutas_formateadas)


def listar_archivos_en_ruta(
    ruta: str | Path,
    incluir_ocultos: bool = True,
    incluir_enlaces: bool = True,
    rutas_absolutas: bool = False
) -> list[str]:
    """
    Retorna una lista de nombres de archivos en la ruta especificada.

    Args:
        ruta (Union[str, Path]): Ruta del directorio a inspeccionar.
        incluir_ocultos (bool): Si incluir archivos ocultos (que empiezan con '.').
        incluir_enlaces (bool): Si incluir enlaces simbólicos a archivos.
        rutas_absolutas (bool): Si retornar rutas absolutas o solo nombres.

    Returns:
        List[str]: Lista de nombres o rutas de archivos.

    Raises:
        FileNotFoundError: Si la ruta no existe.
        NotADirectoryError: Si la ruta no es un directorio.
        PermissionError: Si no se tienen permisos para leer el directorio.

    Example:
        >>> archivos = listar_archivos_en_ruta('/tmp', incluir_ocultos=False)
    """
    # Convertir a Path para un manejo más robusto
    path = Path(ruta)

    # Validaciones
    if not path.exists():
        raise FileNotFoundError(f"La ruta especificada no existe: {ruta}")

    if not path.is_dir():
        raise NotADirectoryError(f"La ruta especificada no es un directorio: {ruta}")

    try:
        archivos = []
        for item in path.iterdir():
            # Verificar si es archivo
            es_archivo = item.is_file()

            # Si es enlace simbólico, decidir si incluirlo
            if item.is_symlink():
                es_archivo = incluir_enlaces and item.resolve().is_file()

            # Verificar si es oculto
            if not incluir_ocultos and item.name.startswith('.'):
                continue

            if es_archivo:
                if rutas_absolutas:
                    archivos.append(str(item.absolute()))
                else:
                    archivos.append(item.name)

        return archivos

    except PermissionError as e:
        raise PermissionError(f"No se tienen permisos para leer el directorio: {ruta}") from e


def listar_archivos_con_logging(
    ruta: str | Path,
    incluir_ocultos: bool = False,
    recursive: bool = False,
    logger: logging.Logger | None = None
) -> list[Path]:
    """
    Lista archivos con logging detallado y manejo de errores robusto.

    Args:
        ruta: Directorio a listar
        incluir_ocultos: Incluir archivos ocultos
        recursive: Buscar recursivamente
        logger: Logger para registrar eventos (crea uno por defecto)

    Returns:
        List[Path]: Lista de rutas de archivos
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    path = Path(ruta)

    # Validaciones con logging
    if not path.exists():
        logger.error(f"Ruta no existe: {ruta}")
        raise FileNotFoundError(f"La ruta no existe: {ruta}")

    if not path.is_dir():
        logger.error(f"No es directorio: {ruta}")
        raise NotADirectoryError(f"No es un directorio: {ruta}")

    archivos = []
    errores = []

    try:
        # Listar archivos
        iterador = path.rglob('*') if recursive else path.glob('*')

        for item in iterador:
            try:
                if not item.is_file():
                    continue

                if not incluir_ocultos and item.name.startswith('.'):
                    continue

                archivos.append(item)

            except PermissionError as e:
                logger.warning(f"Sin permisos para acceder a {item}: {e}")
                errores.append(str(item))
            except Exception as e:
                logger.error(f"Error inesperado con {item}: {e}")
                errores.append(str(item))

        # Log de resumen
        logger.info(f"Listados {len(archivos)} archivos en {path}")
        if errores:
            logger.warning(f"{len(errores)} archivos no pudieron ser accedidos")

        return archivos

    except PermissionError as e:
        logger.error(f"Sin permisos para leer el directorio {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al listar {path}: {e}")
        raise


def listar_nombres_sin_extension(
        ruta: str | Path,
        incluir_ocultos: bool = False,
        extensiones: list[str] | None = None,
        lowercase: bool = False
) -> list[str]:
    """
    Retorna una lista con los nombres de archivos sin extensión desde la ruta dada.

    Args:
        ruta (Union[str, Path]): Ruta del directorio a inspeccionar.
        incluir_ocultos (bool): Si incluir archivos ocultos (que empiezan con '.').
        extensiones (Optional[List[str]]): Lista de extensiones a incluir.
            Ej: ['.py', '.txt'] - si es None, incluye todas.
        lowercase (bool): Convertir nombres a minúsculas.

    Returns:
        List[str]: Lista de nombres de archivos sin extensión.

    Raises:
        FileNotFoundError: Si la ruta no existe.
        NotADirectoryError: Si la ruta no es un directorio.
        PermissionError: Si no se tienen permisos para leer.

    Examples:
        >>> archivos = listar_nombres_sin_extension('./data', extensiones=['.txt'])
        >>> print(archivos)  # ['archivo1', 'archivo2']
    """
    path = Path(ruta)

    # Validaciones
    if not path.exists():
        raise FileNotFoundError(f"La ruta especificada no existe: {ruta}")

    if not path.is_dir():
        raise NotADirectoryError(f"La ruta especificada no es un directorio: {ruta}")

    # Normalizar extensiones
    if extensiones is not None:
        extensiones = [ext if ext.startswith('.') else f'.{ext}' for ext in extensiones]

    try:
        nombres = []
        for item in path.iterdir():
            # Verificar si es archivo (no directorio)
            if not item.is_file():
                continue

            # Verificar ocultos
            if not incluir_ocultos and item.name.startswith('.'):
                continue

            # Verificar extensiones
            if extensiones is not None:
                ext = item.suffix.lower()
                if ext not in extensiones:
                    continue

            # Obtener nombre sin extensión
            nombre = item.stem  # Path.stem es más limpio que os.path.splitext

            # Aplicar formato
            if lowercase:
                nombre = nombre.lower()

            nombres.append(nombre)

        # Eliminar duplicados manteniendo orden
        return list(dict.fromkeys(nombres))

    except PermissionError as e:
        raise PermissionError(f"No se tienen permisos para leer el directorio: {ruta}") from e


def concatenar_lista_a_string(lista_valores, prefijo_a_concatenar):
    """
    Recibe una lista de valores y un prefijo string.
    Concatena el prefijo a cada valor de la lista y luego une todos
    los elementos resultantes en un único string, separados por una coma y un salto de línea.

    Args:
        lista_valores (list): La lista de valores (por ejemplo, nombres de archivo).
        prefijo_a_concatenar (str): El string que se concatenará a cada valor.

    Returns:
        str: Un único string que contiene todos los elementos concatenados,
             separados por una coma, un salto de línea y comillas dobles.

    Examples:
        >>> prefijo = "garantias-bankgar/Datos_procesados/Garantias/2026/04/20260423/"
        >>> list_documents = concatenar_lista_a_string(list_archivos, prefijo)
    """
    # 1. Concatenar el prefijo a cada valor de la lista
    # lista_concatenada = [f'"{prefijo_a_concatenar}{valor}.pdf"' for valor in lista_valores]
    # lista_concatenada = [f'"{prefijo_a_concatenar}{valor},"' for valor in lista_valores]
    lista_concatenada = [f'{prefijo_a_concatenar}{valor},' for valor in lista_valores]

    # 2. Unir todos los elementos de la lista_concatenada en un solo string
    #    separados por una coma, un salto de línea y una comilla doble.
    #    Se agrega una coma y un salto de línea después de cada elemento,
    #    excepto el último, para que coincida con el formato del ejemplo.

    # Nota: El ejemplo de retorno que proporcionaste tiene una coma después de cada línea,
    # por lo que el separador usado será ',\n'.

    # resultado_string = ',\n'.join(lista_concatenada)
    # resultado_string = ','.join(lista_concatenada)
    resultado_string = ''.join(lista_concatenada)

    return resultado_string

# ==============================================================================
# EJEMPLOS DE USO Y PRUEBAS
# ==============================================================================
if __name__ == '__main__':
    print("Iniciando pruebas de la función generar_rutas_garantias...\n")

    # 1. Prueba de éxito con archivos reales usando un directorio temporal
    print("--- CASO 1: Carpeta con archivos ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)

        # Crear archivos simulados para la prueba
        (dir_path / "datos_cliente_A.csv").touch()
        (dir_path / "reporte_mensual.pdf").touch()
        (dir_path / "log_transacciones.txt").touch()

        resultado = generar_rutas_garantias(dir_path)
        print("Resultado generado exitosamente:")

        # Imprimimos separando por comas y saltos de línea para facilitar la lectura
        # en la consola, aunque el string subyacente es solo separado por comas
        for ruta in resultado.split(","):
            print(f" -> {ruta}")

    # 2. Prueba con carpeta vacía
    print("\n--- CASO 2: Carpeta vacía ---")
    with tempfile.TemporaryDirectory() as temp_dir_vacio:
        resultado_vacio = generar_rutas_garantias(temp_dir_vacio)
        if resultado_vacio == "":
            print("Éxito: La función retornó una cadena vacía para una carpeta sin archivos.")

    # 3. Prueba de manejo de excepciones: Ruta inexistente
    print("\n--- CASO 3: Ruta inexistente ---")
    ruta_falsa = Path("/ruta/que/definitivamente/no/existe/12345")
    try:
        generar_rutas_garantias(ruta_falsa)
    except FileNotFoundError as e:
        print(f"Excepción capturada correctamente: {e}")

    # 4. Prueba de manejo de excepciones: La ruta es un archivo, no una carpeta
    print("\n--- CASO 4: Ruta es un archivo ---")
    with tempfile.NamedTemporaryFile() as temp_file:
        try:
            generar_rutas_garantias(temp_file.name)
        except NotADirectoryError as e:
            print(f"Excepción capturada correctamente: {e}")
