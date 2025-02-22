# File: src/modules/applicant_parser_module.py

from typing import List, Optional, Tuple
from src.models.applicant_profile import ApplicantProfile
from src.modules.applicant_parser.applicant_builder import AbstractApplicantProfileBuilder, ApplicantProfileBuilder
from src.llm_wrappers.llm_providers import LLMProvider, OpenAILLMProvider
from src.persistance.applicant_repository import ApplicantRepository
from src.persistance.file_storage.file_applicant_repository import FileApplicantRepository


class ApplicantParserModule:
    def __init__(self,
                 llm_provider: LLMProvider = None,
                 builder: AbstractApplicantProfileBuilder = None,
                 repository: ApplicantRepository = None
                 ):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        self.builder = builder or ApplicantProfileBuilder(self.llm_provider)
        self.repository = repository or FileApplicantRepository()

    def parse(self, applicant_id: str, applicant_texts: List[str]) -> ApplicantProfile:
        if not applicant_texts:
            return self._fetch_stored_applicant_or_fail(applicant_id)

        new_raw_text = self._combine_new_texts(applicant_texts)
        stored_raw, _ = self._get_existing_applicant(applicant_id)

        merged_raw = self._merge_texts(stored_raw, new_raw_text) if stored_raw is not None else new_raw_text

        updated_profile = self._build_applicant_profile(merged_raw)
        self.repository.store_applicant(applicant_id, merged_raw, updated_profile)
        return updated_profile


    def _fetch_stored_applicant_or_fail(self, applicant_id: str) -> ApplicantProfile:
        stored = self.repository.get_applicant(applicant_id)
        if stored:
            print("Loading applicant data from repository (no new texts provided).")
            return stored[1]
        else:
            raise ValueError(f"No applicant texts provided and no stored data for applicant_id: {applicant_id}")

    def _get_existing_applicant(self, applicant_id: str) -> Tuple[Optional[str], Optional[ApplicantProfile]]:
        stored = self.repository.get_applicant(applicant_id)
        if stored:
            return stored  # returns (raw_text, applicant_profile)
        return None, None

        # Helper to build an applicant profile using the builder
    def _build_applicant_profile(self, raw_text: str) -> ApplicantProfile:
        return self.builder.add_source("Merged", raw_text).build()

    @staticmethod
    def _merge_texts(existing_raw: str, new_raw: str) -> str:
        return existing_raw + new_raw

    @staticmethod
    def _combine_new_texts(self, applicant_texts: List[str]) -> str:
        return ''.join(applicant_texts)
