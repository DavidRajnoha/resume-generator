import json
import os

import pytest

from src.models.applicant_profile import ApplicantProfile
from src.parsers.applicant_builder import ApplicantProfileBuilder
from src.llm_wrappers.llm_providers import OpenAILLMProvider


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"],
    reason="Skipping integration test because OPENAI_API_KEY is not set"
)
def test_build_integration(applicant_resume_txt, linkedin_profile_txt, applicant_custom_txt, model):
    real_provider = OpenAILLMProvider(model=model, temperature=0.3, max_tokens=1500)
    builder = ApplicantProfileBuilder(real_provider)

    builder.add_source("Resume", applicant_resume_txt)
    builder.add_source("LinkedIn Profile", linkedin_profile_txt)
    builder.add_source("Plain Text", applicant_custom_txt)

    result = builder.build()
    assert isinstance(result, ApplicantProfile)

    print(result.to_json())