from abc import ABC, abstractmethod
from typing import Optional

from src.models.application_data import ApplicationData


class ApplicationRepository(ABC):
    @abstractmethod
    def get_application(self, key: str) -> Optional[ApplicationData]:
        """Retrieve stored application data by a key."""
        pass

    @abstractmethod
    def store_application(self, key: str, application: ApplicationData) -> None:
        """Store or update the application data under the given key."""
        pass



class InMemoryApplicationRepository(ApplicationRepository):
    def __init__(self):
        self._storage = {}  # key: hash -> ApplicationData

    def get_application(self, key: str) -> Optional[ApplicationData]:
        return self._storage.get(key)

    def store_application(self, key: str, application: ApplicationData) -> None:
        self._storage[key] = application