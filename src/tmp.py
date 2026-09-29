#%%
from pathlib import Path

import pandas as pd

from src.utils import logger as log

logger = log.LOGGER
config = log.CONFIG

#%%
logger.info("hello world")
logger.info("variables de configuracion:\n%s", config)

#%%
file_path = Path(config.paths.data.raw) / "house_prices.csv"
if not file_path.exists():
    from src.config import PROJECT_PATH
    file_path = PROJECT_PATH / config.paths.data.raw / "house_prices.csv"

logger.info("Leyendo archivo desde: %s", file_path)
df = pd.read_csv(file_path)
logger.info("Archivo cargado exitosamente con dimensiones: %s", df.shape)

#%%
df.head()