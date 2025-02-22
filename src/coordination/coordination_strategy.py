from typing import List, Tuple, Optional
from abc import ABC, abstractmethod

from src.builders.resume_builder import ResumeBuilder
from src.llm_wrappers.llm_providers import OpenAILLMProvider, LLMProvider
from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData
from src.parsers.application_parser import PlainTextParser, ApplicationParser
from src.parsers.applicant_builder import ApplicantProfileBuilder, AbstractApplicantProfileBuilder
from src.persistance.file_storage.file_applicant_repository import FileApplicantRepository
from src.persistance.file_storage.file_application_repository import FileApplicationRepository
from src.persistance.utils import compute_hash
from src.utils.latex_to_pdf import generate_pdf

class CoordinationStrategy(ABC):
    @abstractmethod
    def load_applicant_data(self, paths: List[str], retry: int = 1) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def load_application_data(self, path: str, retry: int = 1) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_applicant_data(self, applicant_id: str, applicant_texts: List[str],
                             llm_provider: LLMProvider = None, retry: int = 1) -> ApplicantProfile:
        raise NotImplementedError

    @abstractmethod
    def parse_application_data(self, application_text: str,
                               llm_provider: LLMProvider = None, retry: int = 1) -> ApplicationData:
        raise NotImplementedError

    @abstractmethod
    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData,
                     llm_provider: LLMProvider = None, retry: int = 1) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_pdf(self, resume_latex: str, output_path: str, retry: int = 1):
        raise NotImplementedError


class LocalCoordinationStrategy(CoordinationStrategy):
    def __init__(self,
                 llm_provider: LLMProvider = None,
                 application_parser: ApplicationParser = None,
                 applicant_builder: AbstractApplicantProfileBuilder = None,
                 resume_builder: ResumeBuilder = None,
                 application_repository=None,
                 applicant_repository=None):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        self.application_parser = application_parser or PlainTextParser(self.llm_provider)
        self.applicant_builder = applicant_builder or ApplicantProfileBuilder(self.llm_provider)
        # self.resume_builder = resume_builder or ResumeBuilder(llm_provider)
        self.application_repo = application_repository or FileApplicationRepository()
        self.applicant_repo = applicant_repository or FileApplicantRepository()


    @staticmethod
    def load_text(path: str) -> str:
        with open(path, "r") as file:
            return file.read()

    def load_applicant_data(self, paths: List[str], retry: int = 1) -> List[str]:
        print(f"[LocalCoordinationStrategy] load_applicant_data retry {retry}")
        applicant_texts = []
        for path in paths:
            applicant_texts.append(LocalCoordinationStrategy.load_text(path))
        return applicant_texts

    def load_application_data(self, path: str, retry: int = 1) -> str:
        print(f"[LocalCoordinationStrategy] load_application_data retry {retry}")
        return LocalCoordinationStrategy.load_text(path)

    def parse_application_data(self, application_text: str,
                               llm_provider: LLMProvider = None, retry: int = 1) -> ApplicationData:
        print(f"[LocalCoordinationStrategy] parse_application_data retry {retry}")
        key = compute_hash(application_text)
        stored_application = self.application_repo.get_application(key)
        if stored_application:
            print("Loading application data from repository.")
            return stored_application

        application_data = self.application_parser.parse(application_text)
        self.application_repo.store_application(key, application_data)
        return application_data

    def parse_applicant_data(self, applicant_id: str, applicant_texts: List[str],
                             llm_provider: LLMProvider = None, retry: int = 1) -> ApplicantProfile:
        print(f"[LocalCoordinationStrategy] parse_applicant_data retry {retry}")
        if not applicant_texts:
            return self._fetch_stored_applicant_or_fail(applicant_id)

        new_raw_text = self._combine_new_texts(applicant_texts)
        stored_raw, _ = self._get_existing_applicant(applicant_id)

        merged_raw = self._merge_texts(stored_raw, new_raw_text) if stored_raw is not None else new_raw_text

        updated_profile = self._build_applicant_profile(merged_raw)
        self.applicant_repo.store_applicant(applicant_id, merged_raw, updated_profile)
        return updated_profile

    # Helper to fetch stored applicant data or raise an error
    def _fetch_stored_applicant_or_fail(self, applicant_id: str) -> ApplicantProfile:
        stored = self.applicant_repo.get_applicant(applicant_id)
        if stored:
            print("Loading applicant data from repository (no new texts provided).")
            return stored[1]
        else:
            raise ValueError(f"No applicant texts provided and no stored data for applicant_id: {applicant_id}")

    # Helper to combine new texts into one string
    def _combine_new_texts(self, applicant_texts: List[str]) -> str:
        return ''.join(applicant_texts)

    # Helper to get any existing applicant data
    def _get_existing_applicant(self, applicant_id: str) -> Tuple[Optional[str], Optional[ApplicantProfile]]:
        stored = self.applicant_repo.get_applicant(applicant_id)
        if stored:
            return stored  # returns (raw_text, applicant_profile)
        return (None, None)

    # Helper to merge new and existing raw texts
    def _merge_texts(self, existing_raw: str, new_raw: str) -> str:
        return existing_raw + new_raw

    # Helper to build an applicant profile using the builder
    def _build_applicant_profile(self, raw_text: str) -> ApplicantProfile:
        return self.applicant_builder.add_source("Merged", raw_text).build()

    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData,
                     llm_provider: LLMProvider = None, retry: int = 1) -> str:
        if llm_provider is None:
            llm_provider = OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        resume_builder = ResumeBuilder(applicant, application, llm_provider)
        return resume_builder.build_resume()

    def generate_pdf(self, resume_latex: str, output_path: str, retry: int = 1):
        print(f"[LocalCoordinationStrategy] generate_pdf retry {retry}")
        generate_pdf(resume_latex, output_path)
