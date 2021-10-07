import itertools

import dacite
import toml
from loguru import logger
from typing import Iterable


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


def show_config(config, fields: Iterable[str]):
    logger.info("[Configuration]")
    for field in itertools.chain(config.__dataclass_fields__.keys(), fields):
        value = getattr(config, field)
        if isinstance(value, bool):
            logger.info(f"{field:16} => {'enabled' if value else 'disabled'}")
        elif isinstance(value, (float, int)):
            logger.info(f"{field:16} => {value:5.2f} mm")
        else:
            logger.info(f"{field:16} => {value}")