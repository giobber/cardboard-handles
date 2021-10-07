import dacite
import toml
from loguru import logger


def load_toml(path, model):
    try:
        with open(path, "rt") as fp:
            raw = toml.load(fp)
        return dacite.from_dict(model, raw)
    except dacite.exceptions.DaciteError as e:
        logger.error(e)
        exit()
    except FileNotFoundError:
        logger.error(f"File {path} not found")
        exit()
