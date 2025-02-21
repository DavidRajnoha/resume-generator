from typing import List
from abc import ABC, abstractmethod

from src.builders.resume_builder import ResumeBuilder
from src.llm_wrappers.llm_providers import OpenAILLMProvider, LLMProvider
from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData
from src.parsers.application_parser import PlainTextParser, ApplicationParser
from src.parsers.applicant_builder import ApplicantProfileBuilder, AbstractApplicantProfileBuilder
from src.utils.latex_to_pdf import generate_pdf

class CoordinationStrategy(ABC):
    @abstractmethod
    def load_applicant_data(self, paths: List[str], retry: int = 1) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def load_application_data(self, path: str, retry: int = 1) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_applicant_data(self, applicant_texts: List[str],
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
                 resume_builder: ResumeBuilder = None):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        self.application_parser = application_parser or PlainTextParser(self.llm_provider)
        self.applicant_builder = applicant_builder or ApplicantProfileBuilder(self.llm_provider)
        # self.resume_builder = resume_builder or ResumeBuilder(llm_provider)

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
        return self.application_parser.parse(application_text)

    def parse_applicant_data(self, applicant_texts: List[str],
                             llm_provider: LLMProvider = None, retry: int = 1) -> ApplicantProfile:
        print(f"[LocalCoordinationStrategy] parse_applicant_data retry {retry}")
        applicant_resume_text = applicant_texts[0]
        applicant_custom_text = applicant_texts[1]
        return (self.applicant_builder.add_source("Resume", applicant_resume_text)
                                .add_source("Custom Text", applicant_custom_text)
                                .build())

    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData,
                     llm_provider: LLMProvider = None, retry: int = 1) -> str:
        if llm_provider is None:
            llm_provider = OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        resume_builder = ResumeBuilder(applicant, application, llm_provider)
        return resume_builder.build_resume()

    def generate_pdf(self, resume_latex: str, output_path: str, retry: int = 1):
        print(f"[LocalCoordinationStrategy] generate_pdf retry {retry}")
        generate_pdf(resume_latex, output_path)
