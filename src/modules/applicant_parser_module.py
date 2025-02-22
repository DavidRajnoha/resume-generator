from typing import List
from src.models.applicant_profile import ApplicantProfile
from src.modules.applicant_parser.applicant_builder import AbstractApplicantProfileBuilder, ApplicantProfileBuilder
from src.llm_wrappers.llm_providers import LLMProvider, OpenAILLMProvider
from src.persistance.applicant_repository import ApplicantRepository
from src.persistance.file_storage.file_applicant_repository import FileApplicantRepository
from src.persistance.adapters.applicant_repository_adapter import ApplicantRepositoryAdapter

class ApplicantParserModule:
    def __init__(self,
                 llm_provider: LLMProvider = None,
                 builder: AbstractApplicantProfileBuilder = None,
                 repository: ApplicantRepository = None,
                 repo_adapter: ApplicantRepositoryAdapter = None,):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        self.builder = builder or ApplicantProfileBuilder(self.llm_provider)
        self.repository = repository or FileApplicantRepository()
        self.repo_adapter = repo_adapter or ApplicantRepositoryAdapter(self.repository)

    def parse(self, applicant_id: str, applicant_texts: List[str]) -> ApplicantProfile:
        """
        Parse the applicant texts and return the updated applicant profile.
        :param applicant_id:
        :param applicant_texts:
        :raises ValueError: If no applicant texts are provided and no stored data is found.
        :return:
        """
        if not applicant_texts:
            return self.repo_adapter.fetch_applicant_or_fail(applicant_id)
        # Combine the new texts.
        new_raw_text = ''.join(applicant_texts)
        # Merge with any stored raw text.
        merged_raw = self.repo_adapter.merge_raw_texts(applicant_id, new_raw_text)
        # Use the builder (which remains independent) to produce the applicant profile.
        updated_profile = self.builder.add_source("Merged", merged_raw).build()
        # Store the updated data.
        self.repo_adapter.store_applicant(applicant_id, merged_raw, updated_profile)
        return updated_profile
