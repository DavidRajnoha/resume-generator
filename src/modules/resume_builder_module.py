# File: src/modules/resume_builder_module.py

from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData
from src.modules.resume_builder.resume_builder import ResumeBuilder
from src.llm_wrappers.llm_providers import LLMProvider, OpenAILLMProvider


class ResumeBuilderModule:
    def __init__(self, llm_provider: LLMProvider = None):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)

    def build(self, applicant: ApplicantProfile, application: ApplicationData) -> str:
        resume_builder = ResumeBuilder(applicant, application, self.llm_provider)
        return resume_builder.build_resume()
