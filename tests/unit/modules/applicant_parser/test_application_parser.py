import pytest

from src.llm_wrappers.llm_providers import LLMProvider
from src.modules.application_parser.application_parser import PlainTextParser


class MockLLMProvider(LLMProvider):
    def complete(self, prompt: str) -> str:
        return '''{
            "position_information": {
                "job_title": "Software Engineer",
                "department": "Engineering",
                "location": "Remote",
                "employment_type": "Full-Time",
                "description": "Develop and maintain software.",
                "responsibilities": ["Write code", "Review code"],
                "requirements": ["Python", "Teamwork"],
                "posted_date": "2025-02-19",
                "closing_date": "2025-03-01"
            },
            "company_profile": {
                "name": "Tech Corp",
                "website": "https://techcorp.example.com",
                "description": "A leading technology company.",
                "industry": "Technology",
                "size": "200-500 employees"
            },
            "custom_sections": [
                {
                    "section_title": "Cover Letter",
                    "content": "I am excited to apply."
                }
            ],
            "extra_text": ["Additional note"]
        }'''

@pytest.fixture
def fake_parser():
    return PlainTextParser(MockLLMProvider())

def test_parse_returns_correct_data(fake_parser):
    raw_text = "Irrelevant raw text for unit test."
    application_data = fake_parser.parse(raw_text)

    assert application_data.position_information.job_title == "Software Engineer"
    assert application_data.company_profile.name == "Tech Corp"
    assert len(application_data.custom_sections) == 1
    assert application_data.custom_sections[0].section_title == "Cover Letter"
    assert application_data.extra_text[0] == "Additional note"