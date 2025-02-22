import os

import pytest

from src.modules.application_parser.application_parser import PlainTextParser


@pytest.fixture
def raw_text():
    return """
    Software Engineer needed at Tech Corp.
    Department: Engineering
    Location: Remote
    Employment Type: Full-Time
    Job Description: Develop and maintain software solutions.
    Responsibilities: Write code, Review code.
    Requirements: Proficiency in Python, Teamwork.
    Posted Date: 2025-02-19
    Closing Date: 2025-03-01

    Cover Letter:
    I am excited to apply for this position.

    Additional Notes:
    Looking forward to contributing to the team.
    """


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"],
    reason="Skipping integration test because OPENAI_API_KEY is not set"
)
def test_parse_with_real_llm(application_raw_text, model):
    # Replace with your real LLM provider implementation
    from src.llm_wrappers.llm_providers import OpenAILLMProvider  # Adjust based on your actual provider

    real_llm = OpenAILLMProvider(model=model, temperature=0.3, max_tokens=1500)
    parser = PlainTextParser(real_llm)

    application_data = parser.parse(raw_text_extended)

    assert application_data.position_information.job_title is not None
    assert application_data.company_profile.name is not None
    # assert len(application_data.custom_sections) >= 1
    print(application_data.to_json())  # Optional: Print parsed JSON for debugging
