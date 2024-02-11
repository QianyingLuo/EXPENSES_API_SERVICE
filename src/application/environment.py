import os
from . import log

from typing import Optional


logger = log.get_logger(__name__)

database_environment_variables: dict[str, str] = {}
jwt_environment_variables: dict[str, str] = {}
environment_variables: dict[str, str] = {}

def get_mandatory_environment_variable(key: str, environment_list: dict[str, str]) -> str:
    value: Optional[str] = os.environ.get(key, None)

    if not value:
        raise ValueError(f"{key} environment variable is mandatory")

    environment_list[key] = value
    return value


def get_environment_variable(key: str, default_value: str, environment_list: dict[str, str]) -> Optional[str]:
    value: str = os.environ.get(key, default=default_value)
    environment_list[key] = value
    return value


def get_environment() -> dict[str, str]:
    return environment_variables


def read_environment(): 
    log_environment()

def read_database_environment():
    get_mandatory_environment_variable("MONGO_HOST", database_environment_variables)
    get_mandatory_environment_variable("MONGO_USER", database_environment_variables)
    get_mandatory_environment_variable("MONGO_PASSWORD", database_environment_variables)
    get_mandatory_environment_variable("MONGO_DATABASE", database_environment_variables)
    return database_environment_variables

def read_jwt_environment():
    get_mandatory_environment_variable("TOKEN_SECRET", jwt_environment_variables)


def log_environment() -> None:
    logger.debug(f"SYSTEM ENVIRONMENT VARIABLES:")
    for key, value in environment_variables.items():
        logger.debug(f"      {key}: {value}")