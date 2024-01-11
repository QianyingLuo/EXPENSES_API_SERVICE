import os
from .. import logger

logger = logger.getLogger(__name__)

_variables_list: dict[str, str] = {}

def store_environment_variable(key: str, default: str):
    value = os.environ.get(key, default)
    _variables_list[key] = value
    return value

DB_HOST = store_environment_variable("DB_HOST", "localhost")
DB_PORT = store_environment_variable("DB_PORT", "3306")
DB_USER = store_environment_variable("DB_USER", "root")
DB_PASSWORD = store_environment_variable("DB_PASSWORD", "")

logger.debug("Environment variables:")
for key, value in _variables_list.items():
    logger.debug(f"     {key}: {value}")


