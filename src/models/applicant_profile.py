import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class PersonalInformation:
    full_name: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    linkedin: str = ""
    website: str = ""

@dataclass
class Education:
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str = ""

@dataclass
class WorkExperience:
    title: str = ""
    company: str = ""
    location: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: List[str] = field(default_factory=list)

@dataclass
class VolunteerExperience:
    role: str = ""
    organization: str = ""
    location: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: List[str] = field(default_factory=list)

@dataclass
class Project:
    name: str = ""
    description: str = ""
    role: str = ""
    technologies: List[str] = field(default_factory=list)
    link: str = ""

@dataclass
class Certification:
    name: str = ""
    issuing_organization: str = ""
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: str = ""
    credential_url: str = ""

@dataclass
class Award:
    title: str = ""
    issuer: str = ""
    date: Optional[str] = None
    description: str = ""

@dataclass
class Language:
    language: str = ""
    proficiency: str = ""  # e.g., Native, Fluent, Intermediate

@dataclass
class Publication:
    title: str = ""
    publisher: str = ""
    publication_date: Optional[str] = None
    url: str = ""
    description: str = ""

@dataclass
class CoverLetterStory:
    title: str = ""
    content: str = ""

@dataclass
class ApplicantProfile:
    personal_info: PersonalInformation = field(default_factory=PersonalInformation)
    professional_summary: str = ""
    skills: List[str] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    work_experience: List[WorkExperience] = field(default_factory=list)
    volunteer_experience: List[VolunteerExperience] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    awards: List[Award] = field(default_factory=list)
    languages: List[Language] = field(default_factory=list)
    publications: List[Publication] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    cover_letter_stories: List[CoverLetterStory] = field(default_factory=list)

    @staticmethod
    def from_json(data: dict):
        """Creates an ApplicantProfile object from a JSON/dict representation."""
        personal_info = PersonalInformation(**data.get('personal_info', {}))
        professional_summary = data.get('professional_summary', "")
        skills = data.get('skills', [])
        education = [Education(**item) for item in data.get('education', [])]
        work_experience = [WorkExperience(**item) for item in data.get('work_experience', [])]
        volunteer_experience = [VolunteerExperience(**item) for item in data.get('volunteer_experience', [])]
        projects = [Project(**item) for item in data.get('projects', [])]
        certifications = [Certification(**item) for item in data.get('certifications', [])]
        awards = [Award(**item) for item in data.get('awards', [])]
        languages = [Language(**item) for item in data.get('languages', [])]
        publications = [Publication(**item) for item in data.get('publications', [])]
        interests = data.get('interests', [])
        cover_letter_stories = [CoverLetterStory(**item) for item in data.get('cover_letter_stories', [])]

        return ApplicantProfile(
            personal_info=personal_info,
            professional_summary=professional_summary,
            skills=skills,
            education=education,
            work_experience=work_experience,
            volunteer_experience=volunteer_experience,
            projects=projects,
            certifications=certifications,
            awards=awards,
            languages=languages,
            publications=publications,
            interests=interests,
            cover_letter_stories=cover_letter_stories
        )

    def to_json(self) -> str:
        """Convert the ApplicantProfile instance to a JSON string."""
        return json.dumps(asdict(self), indent=2)