"""
Coordinating the process of the program
"""
from abc import abstractmethod
from typing import Optional, List

from src.builders.resume_builder import ResumeBuilder
from src.llm_wrappers.llm_providers import OpenAILLMProvider, LLMProvider
from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData
from src.parsers.application_parser import PlainTextParser
from src.parsers.applicant_builder import ApplicantProfileBuilder
from src.utils.latex_to_pdf import generate_pdf

class CoordinationStrategy:
    @abstractmethod
    def load_applicant_data(self, *paths):
        raise NotImplementedError

    @abstractmethod
    def load_application_data(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def parse_applicant_data(self, applicant_texts: list[str], llm_provider: LLMProvider = None):
        raise NotImplementedError

    @abstractmethod
    def parse_application_data(self, application_text: str, llm_provider: LLMProvider = None):
        raise NotImplementedError

    @abstractmethod
    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData, llm_provider: LLMProvider = None):
        raise NotImplementedError

    @abstractmethod
    def generate_pdf(self, resume_latex: str, output_path: str):
        raise NotImplementedError


class LocalCoordinationStrategy(CoordinationStrategy):
    @staticmethod
    def load_text(path: str) -> str:
        with open(path, "r") as file:
            return file.read()

    def load_applicant_data(self, paths: List[str]):
        applicant_texts = []
        for path in paths:
            applicant_texts.append(LocalCoordinationStrategy.load_text(path))
        return applicant_texts

    def load_application_data(self, path: str):
        return LocalCoordinationStrategy.load_text(path)

    def parse_application_data(self, application_text, llm_provider: LLMProvider = None):
        if llm_provider is None:
            llm_provider = OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=1500)
        application_parser = PlainTextParser(llm_provider)
        return application_parser.parse(application_text)

    def parse_applicant_data(self, applicant_texts, llm_provider: LLMProvider = None):
        if llm_provider is None:
            llm_provider = OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=1500)
        applicant_builder = ApplicantProfileBuilder(llm_provider)
        applicant_resume_text = applicant_texts[0]
        applicant_custom_text = applicant_texts[1]
        return (applicant_builder.add_source("Resume", applicant_resume_text)
                                .add_source("Custom Text", applicant_custom_text)
                                .build())

    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData, llm_provider: LLMProvider = None):
        if llm_provider is None:
            llm_provider = OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        resume_builder = ResumeBuilder(applicant, application, llm_provider)
        return  resume_builder.build_resume()

    def generate_pdf(self, resume_latex, output_path: str):
        generate_pdf(resume_latex, output_path)

class CoordinatingManager:
    pass

class LocalCoordinatingManager(CoordinatingManager):
    def __init__(self):
        self.coordination_strategy = LocalCoordinationStrategy()
        self.applicant_texts = []
        self.application_text = None
        self.applicant: Optional[ApplicantProfile] = None
        self.application: Optional[ApplicationData] = None
        self.resume_latex: Optional[str] = None


    def run(self, applicant_paths: List[str], application_path: str, output_path: str):
        """
        Generate a resume from the provided application and applicant data.
        """
        self.applicant_texts = (self.coordination_strategy.
                                load_applicant_data(applicant_paths))

        self.application_text = (self.coordination_strategy.
                                 load_application_data(application_path))

        self.applicant = (self.coordination_strategy.
                          parse_applicant_data(self.applicant_texts))

        self.application = (self.coordination_strategy.
                            parse_application_data(self.application_text))

        self.resume_latex = (self.coordination_strategy.
                                build_resume(self.applicant, self.application))

        self.coordination_strategy.generate_pdf(
            self.resume_latex,
            output_path)
