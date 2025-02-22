import os
import pickle
from typing import Optional, Tuple
from src.models.applicant_profile import ApplicantProfile
from src.persistance.applicant_repository import ApplicantRepository

class FileApplicantRepository(ApplicantRepository):
    def __init__(self, storage_dir: str = "applicant_data"):
        """
        Initialize the repository using a directory for storing applicant data.
        """
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _filepath(self, applicant_id: str) -> str:
        """
        Generate a file path for a given applicant_id.
        Basic sanitization is applied to ensure a safe file name.
        """
        safe_id = applicant_id.replace("/", "_")
        return os.path.join(self.storage_dir, f"{safe_id}.pkl")

    def get_applicant(self, applicant_id: str) -> Optional[Tuple[str, ApplicantProfile]]:
        """
        Retrieve the stored (raw_text, applicant_profile) tuple for the given applicant_id.
        Returns None if no data is found.
        """
        filepath = self._filepath(applicant_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        return data

    def store_applicant(self, applicant_id: str, raw_text: str, applicant: ApplicantProfile) -> None:
        """
        Store the (raw_text, applicant_profile) tuple for the given applicant_id.
        """
        filepath = self._filepath(applicant_id)
        data = (raw_text, applicant)
        with open(filepath, "wb") as f:
            pickle.dump(data, f)
