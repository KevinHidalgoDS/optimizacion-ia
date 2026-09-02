import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class PathsData(BaseModel):
    raw: str
    interim: str
    processed: str
    external: str

class Paths(BaseModel):
    data: PathsData

class Config(BaseModel):
    project: dict
    paths: Paths


def load_config(path: str = "config/config.yaml") -> Config:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(**raw)
