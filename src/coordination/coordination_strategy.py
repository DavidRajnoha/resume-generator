from typing import List
from abc import ABC, abstractmethod

from src.models.application_data import ApplicationData
from src.models.applicant_profile import ApplicantProfile


class CoordinationStrategy(ABC):
    @abstractmethod
    def load_applicant_data(self, paths: List[str], retry: int = 1) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def load_application_data(self, path: str, retry: int = 1) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_applicant_data(self, applicant_id: str, applicant_texts: List[str],
                             retry: int = 1) -> ApplicantProfile:
        raise NotImplementedError

    @abstractmethod
    def parse_application_data(self, application_text: str, retry: int = 1) -> ApplicationData:
        raise NotImplementedError

    @abstractmethod
    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData, retry: int = 1) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_cover_letter(self, applicant: ApplicantProfile, application: ApplicationData, retry: int = 1) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_pdf(self, resume_latex: str, output_path: str, retry: int = 1):
        raise NotImplementedError
