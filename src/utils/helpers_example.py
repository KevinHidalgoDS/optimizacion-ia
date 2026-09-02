#%%
#########################################
# Carga básica con PyYAML (dict simple) #
#########################################
# import yaml
# import logging.config
#
#
# def load_config(path="config/config_example.yaml") -> dict:
#     with open(path, "r", encoding="utf-8") as f:
#         return yaml.safe_load(f)

# # src/data/make_dataset.py
# from src.utils.helpers import load_config
#
# config = load_config()
#
# raw_path = config["paths"]["data"]["raw"]
# target_col = config["data"]["target_column"]
# test_size = config["data"]["test_size"]
#
# print(f"Cargando datos desde: {raw_path}")

##################################################
# Acceso seguro con .get() y valores por defecto #
##################################################
# test_size = config.get("data", {}).get("test_size", 0.2)  # 0.2 si no existe

########################################
# Recomendado: validacion con pydantic #
########################################
# src/config.py
# from pydantic import BaseModel
# import yaml
#
# class PathsData(BaseModel):
#     raw: str
#     interim: str
#     processed: str
#     external: str
#
# class Paths(BaseModel):
#     data: PathsData
#
# class DataConfig(BaseModel):
#     target_column: str
#     id_column: str
#     test_size: float
#     validation_size: float
#     categorical_features: list[str]
#     numerical_features: list[str]
#
# class ModelConfig(BaseModel):
#     algorithm: str
#     hyperparameters: dict
#
# class Config(BaseModel):
#     project: dict
#     paths: Paths
#     data: DataConfig
#     model: ModelConfig
#
# def load_config(path: str = "config/config.yaml") -> Config:
#     with open(path, "r", encoding="utf-8") as f:
#         raw = yaml.safe_load(f)
#     return Config(**raw)

# from src.config import load_config
#
# config = load_config()
#
# print(config.data.target_column)        # autocompletado funciona aquí
# print(config.model.hyperparameters)
# print(config.paths.data.raw)

##################################################
# Cargar como variable global (patrón singleton) #
##################################################
# src/config.py
# _config = None
#
# def get_config(path: str = "config/config.yaml") -> Config:
#     global _config
#     if _config is None:
#         _config = load_config(path)
#     return _config
#
# # en cualquier módulo
# from src.config import get_config
#
# config = get_config()
# n_estimators = config.model.hyperparameters["n_estimators"]

############################################
# Combinar con variables de entorno (.env) #
############################################

# # src/config.py
# import os
# from dotenv import load_dotenv
#
# load_dotenv()  # lee .env
#
# api_key = os.environ.get(config.api["api_key_env_var"])  # ej: CHURN_API_KEY

#######################################################################
# Sobrescribir valores desde línea de comandos (útil en pipelines/CI) #
#######################################################################
# import click
# from src.config import load_config
#
# @click.command()
# @click.option("--n-estimators", default=None, type=int)
# def train(n_estimators):
#     config = load_config()
#     if n_estimators:
#         config.model.hyperparameters["n_estimators"] = n_estimators
#     # ... entrenar modelo

# python -m src.models.train_model --n-estimators 500

# |          Tamaño del proyecto         |                                  Enfoque sugerido                                  |
# |:------------------------------------:|:----------------------------------------------------------------------------------:|
# |    Notebook individual / prototipo   |                        yaml.safe_load() directo, dict simple                       |
# |    Proyecto con src/ estructurado    |                   Función load_config() centralizada + singleton                   |
# | Producción / múltiples colaboradores |     Pydantic (o dataclasses + validación manual) para atrapar errores temprano     |
# |    Experimentación con muchos runs   | Hydra, que además permite overrides por línea de comandos y composición de configs |

#%%
# def setup_logging(path="config/logging.yaml"):
#     with open(path, "r", encoding="utf-8") as f:
#         logging.config.dictConfig(yaml.safe_load(f))