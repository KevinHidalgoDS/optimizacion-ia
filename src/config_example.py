# src/config.py
from pydantic import BaseModel
import yaml

class PathsData(BaseModel):
    raw: str
    interim: str
    processed: str
    external: str

class Paths(BaseModel):
    data: PathsData

class DataConfig(BaseModel):
    target_column: str
    id_column: str
    test_size: float
    validation_size: float
    categorical_features: list[str]
    numerical_features: list[str]

class ModelConfig(BaseModel):
    algorithm: str
    hyperparameters: dict

class Config(BaseModel):
    project: dict
    paths: Paths
    data: DataConfig
    model: ModelConfig

def load_config(path: str = "config/config.yaml") -> Config:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(**raw)