import pytest
from src.models.data_factory import DataFactory
from src.models.applicant_profile import (
    ApplicantProfile,
)
from src.models.application_data import (
    ApplicationData,
)


@pytest.fixture
def applicant_json():
    return {
        "personal_info": {
            "full_name": "Test Name",
            "address": "123 Test Ave, Test City, TS",
            "phone": "1234567890",
            "email": "test@example.com",
            "linkedin": "https://linkedin.com/in/test",
            "website": "https://test.com"
        },
        "professional_summary": "A concise professional summary.",
        "skills": ["Python", "Machine Learning"],
        "education": [{
            "institution": "Test University",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "start_date": "2010",
            "end_date": "2014",
            "description": "Studied various topics in CS."
        }],
        "work_experience": [{
            "title": "Software Developer",
            "company": "Test Corp",
            "location": "Test City",
            "start_date": "2015-01",
            "end_date": "2020-01",
            "responsibilities": ["Developed backend systems", "Implemented APIs"]
        }],
        "volunteer_experience": [{
            "role": "Volunteer Developer",
            "organization": "Nonprofit Org",
            "location": "Test City",
            "start_date": "2018-05",
            "end_date": "2019-05",
            "responsibilities": ["Created website for charity"]
        }],
        "projects": [{
            "name": "Test Project",
            "description": "A sample project description.",
            "role": "Lead Developer",
            "technologies": ["Python", "Django"],
            "link": "https://github.com/test/testproject"
        }],
        "certifications": [{
            "name": "Test Certification",
            "issuing_organization": "Certifying Org",
            "issue_date": "2020-06",
            "expiration_date": "2023-06",
            "credential_id": "CERT123",
            "credential_url": "https://example.com/cert/CERT123"
        }],
        "awards": [{
            "title": "Outstanding Achievement",
            "issuer": "Awarding Org",
            "date": "2021",
            "description": "Awarded for outstanding contributions."
        }],
        "languages": [{
            "language": "English",
            "proficiency": "Native"
        }],
        "publications": [{
            "title": "Test Publication",
            "publisher": "Tech Journal",
            "publication_date": "2022-03",
            "url": "https://example.com/pub",
            "description": "Description of the publication."
        }],
        "interests": ["Coding", "Reading"],
        "cover_letter_stories": [{
            "title": "Why I Code",
            "content": "I have always been passionate about solving problems through code."
        }]
    }


@pytest.fixture
def application_json():
    return {
        "position_information": {
            "job_title": "Senior Developer",
            "department": "Engineering",
            "location": "Remote",
            "employment_type": "Full-Time",
            "description": "Develop high-quality software solutions.",
            "responsibilities": ["Design systems", "Code reviews"],
            "requirements": ["Python", "Leadership"],
            "posted_date": "2023-01-01",
            "closing_date": "2023-02-01"
        },
        "company_profile": {
            "name": "Test Company",
            "website": "https://testcompany.com",
            "description": "A company focused on innovative solutions.",
            "industry": "Technology",
            "size": "Medium"
        },
        "custom_sections": [{
            "section_title": "Unique Value Proposition",
            "content": "I bring a combination of technical expertise and creative problem-solving."
        }],
        "extra_text": ["Additional notes from external sources."]
    }


def test_create_applicant_profile(applicant_json):
    profile = DataFactory.create_applicant_profile(applicant_json)

    assert isinstance(profile, ApplicantProfile)
    assert profile.personal_info.full_name == "Test Name"
    assert profile.personal_info.email == "test@example.com"
    assert profile.professional_summary == "A concise professional summary."
    assert profile.skills == ["Python", "Machine Learning"]

    # Check nested objects
    assert len(profile.education) == 1
    assert profile.education[0].institution == "Test University"

    assert len(profile.work_experience) == 1
    assert profile.work_experience[0].title == "Software Developer"

    assert len(profile.volunteer_experience) == 1
    assert profile.volunteer_experience[0].role == "Volunteer Developer"

    assert len(profile.projects) == 1
    assert profile.projects[0].name == "Test Project"

    assert len(profile.certifications) == 1
    assert profile.certifications[0].name == "Test Certification"

    assert len(profile.awards) == 1
    assert profile.awards[0].title == "Outstanding Achievement"

    assert len(profile.languages) == 1
    assert profile.languages[0].language == "English"

    assert len(profile.publications) == 1
    assert profile.publications[0].title == "Test Publication"

    assert profile.interests == ["Coding", "Reading"]
    assert len(profile.cover_letter_stories) == 1
    assert profile.cover_letter_stories[0].title == "Why I Code"


def test_create_application_data(application_json):
    app_data = DataFactory.create_application_data(application_json)

    assert isinstance(app_data, ApplicationData)
    pos_info = app_data.position_information
    assert pos_info.job_title == "Senior Developer"
    assert pos_info.department == "Engineering"
    assert pos_info.location == "Remote"
    assert pos_info.employment_type == "Full-Time"
    assert pos_info.description == "Develop high-quality software solutions."
    assert pos_info.responsibilities == ["Design systems", "Code reviews"]
    assert pos_info.requirements == ["Python", "Leadership"]
    assert pos_info.posted_date == "2023-01-01"
    assert pos_info.closing_date == "2023-02-01"

    comp_profile = app_data.company_profile
    assert comp_profile.name == "Test Company"
    assert comp_profile.website == "https://testcompany.com"
    assert comp_profile.description == "A company focused on innovative solutions."
    assert comp_profile.industry == "Technology"
    assert comp_profile.size == "Medium"

    assert len(app_data.custom_sections) == 1
    assert app_data.custom_sections[0].section_title == "Unique Value Proposition"

    assert app_data.extra_text == ["Additional notes from external sources."]
