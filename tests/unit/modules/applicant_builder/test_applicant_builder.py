import json

from src.modules.applicant_parser.applicant_builder import ApplicantProfileBuilder
from src.models.applicant_profile import ApplicantProfile

class DummyLLMProvider:
    def complete(self, prompt: str) -> str:
        # Return a JSON string that conforms to the expected schema.
        # This is a minimal valid applicant profile JSON.
        return json.dumps({
            "personal_info": {
                "full_name": "John Doe",
                "address": "123 Main St",
                "phone": "+1 1234567890",
                "email": "john.doe@example.com",
                "linkedin": "https://linkedin.com/in/johndoe",
                "website": "https://johndoe.com"
            },
            "professional_summary": "Experienced software developer.",
            "skills": ["Python", "C++"],
            "education": [{
                "institution": "Tech University",
                "degree": "B.Sc.",
                "field_of_study": "Computer Science",
                "start_date": "2015",
                "end_date": "2019",
                "description": "Studied computer science."
            }],
            "work_experience": [{
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "start_date": "2019",
                "end_date": "Present",
                "responsibilities": ["Developed backend modules"]
            }],
            "volunteer_experience": [],
            "projects": [],
            "certifications": [],
            "awards": [],
            "languages": [{
                "language": "English",
                "proficiency": "Fluent"
            }],
            "publications": [],
            "interests": ["Open source"],
            "cover_letter_stories": [{
                "title": "My Motivation",
                "content": "Passionate about technology."
            }]
        }, indent=2)


def test_build_with_dummy_provider(tmp_path):
    # Create a temporary template file.
    template_content = "Dummy template with [PLACEHOLDER]."
    template_file = tmp_path / "template.tex"
    template_file.write_text(template_content)

    # Instantiate the builder with the DummyLLMProvider.
    dummy_provider = DummyLLMProvider()
    builder = ApplicantProfileBuilder(dummy_provider)

    # Add some sources (they won't affect the dummy output).
    builder.add_source("Resume", "Raw resume text...")
    builder.add_source("LinkedIn Profile", "Raw LinkedIn text...")
    builder.add_source("Plain Text", "Extra cover letter notes...")

    # Build and obtain the JSON output.
    applicant_profile = builder.build()

    # Verify that the output is a dictionary with required keys.
    assert isinstance(applicant_profile, ApplicantProfile)
    assert applicant_profile.personal_info.full_name == "John Doe"
    assert applicant_profile.professional_summary == "Experienced software developer."
    assert applicant_profile.skills == ["Python", "C++"]