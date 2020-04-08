"""Export/Import constants"""
from enum import IntEnum


class Exportation(IntEnum):
    DONE = 0
    EXISTENTCE = 1
    ERROR = 2


class Importation(IntEnum):
    DONE = 0
    REPLICA = 1
    ERROR = 2
