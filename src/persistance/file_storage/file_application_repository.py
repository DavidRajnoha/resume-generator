import os
import pickle
from typing import Optional
from src.models.application_data import ApplicationData
from src.persistance.application_repository import ApplicationRepository

class FileApplicationRepository(ApplicationRepository):
    def __init__(self, storage_dir: str = "application_data"):
        """
        Initialize the repository using a directory for storing application data.
        """
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _filepath(self, application_id: str) -> str:
        """
        Generate a safe file path for a given application_id.
        """
        safe_id = application_id.replace("/", "_")
        return os.path.join(self.storage_dir, f"{safe_id}.pkl")

    def get_application(self, application_id: str) -> Optional[ApplicationData]:
        """
        Retrieve stored application data for the given application_id.
        Returns None if no data is found.
        """
        filepath = self._filepath(application_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        return data

    def store_application(self, application_id: str, application: ApplicationData) -> None:
        """
        Store or update the application data for the given application_id.
        """
        filepath = self._filepath(application_id)
        with open(filepath, "wb") as f:
            pickle.dump(application, f)
