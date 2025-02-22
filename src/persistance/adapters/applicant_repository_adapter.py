from typing import Optional, Tuple
from src.models.applicant_profile import ApplicantProfile
from src.persistance.applicant_repository import ApplicantRepository

class ApplicantRepositoryAdapter:
    def __init__(self, repository: ApplicantRepository):
        self.repository = repository

    def get_existing_applicant(self, applicant_id: str) -> Tuple[Optional[str], Optional[ApplicantProfile]]:
        stored = self.repository.get_applicant(applicant_id)
        return stored if stored is not None else (None, None)

    def merge_raw_texts(self, applicant_id: str, new_raw_text: str) -> str:
        existing_raw, _ = self.get_existing_applicant(applicant_id)
        merged_raw = (existing_raw + new_raw_text) if existing_raw is not None else new_raw_text
        return merged_raw

    def store_applicant(self, applicant_id: str, raw_text: str, applicant_profile: ApplicantProfile) -> None:
        self.repository.store_applicant(applicant_id, raw_text, applicant_profile)

    def fetch_applicant_or_fail(self, applicant_id: str) -> ApplicantProfile:
        stored = self.repository.get_applicant(applicant_id)
        if stored:
            print("Loading applicant data from repository (no new texts provided).")
            return stored[1]
        else:
            raise ValueError(f"No applicant texts provided and no stored data for applicant_id: {applicant_id}")
