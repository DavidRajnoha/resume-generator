from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PositionInformation:
    job_title: str = ""
    department: str = ""
    location: str = ""
    employment_type: str = ""  # e.g., Full-Time, Part-Time, Contract
    description: str = ""
    responsibilities: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    posted_date: Optional[str] = None
    closing_date: Optional[str] = None

@dataclass
class CompanyProfile:
    name: str = ""
    website: str = ""
    description: str = ""
    industry: str = ""
    size: str = ""  # e.g., "50-200 employees" or "Startup"

@dataclass
class CustomSection:
    section_title: str = ""
    content: str = ""


@dataclass
class ApplicationData:
    """
    Holds data specific to a job application, including the parsed job description,
    company details, job-specific cover letter narratives, and any additional custom sections.
    """
    position_information: PositionInformation = field(default_factory=PositionInformation)
    company_profile: CompanyProfile = field(default_factory=CompanyProfile)
    custom_sections: List[CustomSection] = field(default_factory=list)
    extra_text: List[str] = field(default_factory=list)
