from src.models.applicant_profile import (
    ApplicantProfile, PersonalInformation, Education, WorkExperience,
    VolunteerExperience, Project, Certification, Award, Language, Publication, CoverLetterStory
)
from src.models.application_data import (
    ApplicationData, PositionInformation, CompanyProfile, CustomSection
)

class DataFactory:
    @staticmethod
    def create_applicant_profile(data: dict) -> ApplicantProfile:
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

    @staticmethod
    def create_application_data(data: dict) -> ApplicationData:
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