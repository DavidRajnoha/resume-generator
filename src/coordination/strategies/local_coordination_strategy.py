from typing import List

from src.coordination.coordination_strategy import CoordinationStrategy
from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData
from src.modules.application_parser_module import ApplicationParserModule
from src.modules.applicant_parser_module import ApplicantParserModule
from src.modules.resume_builder_module import ResumeBuilderModule
from src.modules.pdf_generator_module import generate_pdf  # still a function, if you wish
from src.modules.applicant_loader import load_applicant_data
from src.modules.application_loader import load_application_data
from src.modules.cover_letter_builder_module import CoverLetterBuilderModule

from src.llm_wrappers.llm_providers import OpenAILLMProvider, LLMProvider


class LocalCoordinationStrategy(CoordinationStrategy):
    def __init__(self,
                 llm_provider: LLMProvider = None,
                 app_parser_module: ApplicationParserModule = None,
                 applicant_parser_module: ApplicantParserModule = None,
                 resume_builder_module: ResumeBuilderModule = None,
                 cover_letter_builder_module: CoverLetterBuilderModule = None,
                 ):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)

        self.llm_provider = llm_provider
        self.app_parser_module = app_parser_module or ApplicationParserModule(llm_provider)
        self.applicant_parser_module = applicant_parser_module or ApplicantParserModule(llm_provider)
        self.resume_builder_module = resume_builder_module or ResumeBuilderModule(llm_provider)
        self.cover_letter_builder_module = cover_letter_builder_module or CoverLetterBuilderModule(llm_provider)


    @staticmethod
    def load_text(path: str) -> str:
        with open(path, "r") as file:
            return file.read()

    def load_applicant_data(self, paths: List[str], retry: int = 1) -> List[str]:
        print(f"[LocalCoordinationStrategy] load_applicant_data retry {retry}")
        return load_applicant_data(paths)

    def load_application_data(self, path: str, retry: int = 1) -> str:
        print(f"[LocalCoordinationStrategy] load_application_data retry {retry}")
        return load_application_data(path)

    def parse_application_data(self, application_text: str, retry: int = 1) -> ApplicationData:
        print(f"[LocalCoordinationStrategy] parse_application_data retry {retry}")
        return self.app_parser_module.parse(application_text)

    def parse_applicant_data(self, applicant_id: str, applicant_texts: List[str], retry: int = 1) -> ApplicantProfile:
        print(f"[LocalCoordinationStrategy] parse_applicant_data retry {retry}")
        return self.applicant_parser_module.parse(applicant_id, applicant_texts)

    def build_resume(self, applicant: ApplicantProfile, application: ApplicationData, retry: int = 1) -> str:
        print(f"[LocalCoordinationStrategy] build_resume retry {retry}")
        return self.resume_builder_module.build(applicant, application)

    def build_cover_letter(self, applicant: ApplicantProfile, application: ApplicationData, retry: int = 1) -> str:
        print(f"[LocalCoordinationStrategy] build_resume retry {retry}")
        return self.cover_letter_builder_module.build()

    def generate_pdf(self, resume_latex: str, output_path: str, retry: int = 1):
        print(f"[LocalCoordinationStrategy] generate_pdf retry {retry}")
        return generate_pdf(resume_latex, output_path)
