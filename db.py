from abc import ABC
from typing import Optional
from datetime import datetime


class Reading(ABC):
    def __int__(self, time: str, name: str, value: float):
        self.time = time
        self.name = name
        self.value = value

    def to_dict(self):
        return self.__dict__


# This is a fake database which stores data in-memory while the process is running
# Feel free to change the data structure to anything else you would like
database: dict[str, dict] = {}


def add_reading(key: str, reading: Reading) -> None:
    """
    Store a reading in the database using the given key
    """
    database[key] = reading.to_dict()


def get_reading(key: str) -> Optional[Reading]:
    """
    Retrieve a reading from the database using the given key
    """
    return database.get(key)
