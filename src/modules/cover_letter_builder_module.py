# File: src/modules/resume_builder_module.py

from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData
from src.modules.cover_letter_builder.cover_letter_builder import CoverLetterBuilder
from src.llm_wrappers.llm_providers import LLMProvider, OpenAILLMProvider


class CoverLetterBuilderModule:
    def __init__(self, llm_provider: LLMProvider = None):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)

    def build(self, applicant: ApplicantProfile, application: ApplicationData) -> str:
        cover_letter_builder = CoverLetterBuilder(applicant, application, self.llm_provider)
        return cover_letter_builder.build_cover_letter()
