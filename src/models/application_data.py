import json
from dataclasses import dataclass, field, asdict
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
    @staticmethod
    def from_json(data: dict):
        """Creates an ApplicationData object from a JSON/dict representation."""
        position_information = PositionInformation(**data.get('position_information', {}))
        company_profile = CompanyProfile(**data.get('company_profile', {}))
        custom_sections = [CustomSection(**item) for item in data.get('custom_sections', [])]
        extra_text = data.get('extra_text', [])

        return ApplicationData(
            position_information=position_information,
            company_profile=company_profile,
            custom_sections=custom_sections,
            extra_text=extra_text
        )

    position_information: PositionInformation = field(default_factory=PositionInformation)
    company_profile: CompanyProfile = field(default_factory=CompanyProfile)
    custom_sections: List[CustomSection] = field(default_factory=list)
    extra_text: List[str] = field(default_factory=list)  # For any additional parsed plain text

    def to_json(self) -> str:
        """Convert the ApplicationData instance to a JSON string."""
        return json.dumps(asdict(self), indent=2)

