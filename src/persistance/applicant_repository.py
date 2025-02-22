from abc import ABC, abstractmethod
from typing import Optional, Tuple
from src.models.applicant_profile import ApplicantProfile

class ApplicantRepository(ABC):
    @abstractmethod
    def get_applicant(self, applicant_id: str) -> Optional[Tuple[str, ApplicantProfile]]:
        """
        Retrieve the stored raw text and applicant profile by applicant ID.
        Returns a tuple (raw_text, applicant_profile) if available.
        """
        pass

    @abstractmethod
    def store_applicant(self, applicant_id: str, raw_text: str, applicant: ApplicantProfile) -> None:
        """
        Store or update the applicant profile along with its raw text.
        """
        pass


class InMemoryApplicantRepository(ApplicantRepository):
    def __init__(self):
        # Maps applicant_id to (raw_text, applicant_profile)
        self._storage = {}

    def get_applicant(self, applicant_id: str) -> Optional[Tuple[str, ApplicantProfile]]:
        return self._storage.get(applicant_id)

    def store_applicant(self, applicant_id: str, raw_text: str, applicant: ApplicantProfile) -> None:
        self._storage[applicant_id] = (raw_text, applicant)
