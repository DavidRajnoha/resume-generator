from dataclasses import dataclass, field
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