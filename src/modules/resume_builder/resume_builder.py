import json
import os

from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData


class LLMCallFailedException(Exception):
    pass

class ResumeBuilder:
    def __init__(self, applicant_data: ApplicantProfile, application_data: ApplicationData, llm_provider,
                 template_path=None):
        """
        :param applicant_data: An object or dict containing applicant data.
                               If an object, it should implement a to_json() method.
        :param application_data: An object or dict containing application/job data.
                                 If an object, it should implement a to_json() method.
        :param template_path: Path to the LaTeX resume template with placeholders.
        """
        if template_path is None:
            source_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(source_dir, "templates", "resume_template.tex")


        self.applicant_data = applicant_data
        self.application_data = application_data
        with open(template_path, "r") as f:
            self.template = f.read()
        self.llm_provider = llm_provider

    def _get_json(self, data) -> str:
        """
        Convert the provided data to a JSON string.
        If the data object implements a to_json() method, that will be used;
        otherwise, the data is assumed to be JSON-serializable.
        """
        if hasattr(data, "to_json"):
            return data.to_json()
        else:
            return json.dumps(data, indent=2)

    def build_resume(self) -> str:
        """
        Build a personalized resume by providing the raw LaTeX template and JSON data
        to the LLM. The LLM is instructed to merge the two and output a final,
        fully populated, valid LaTeX resume.

        :return: A string containing the final LaTeX resume.
        """
        applicant_json = self._get_json(self.applicant_data)
        application_json = self._get_json(self.application_data)

        prompt = (
            "You are an expert resume builder that produces strategic, tailored LaTeX resumes. "
            "Using the applicant data and specific job application data provided below, create a highly customized "
            "resume that aligns the candidate's experience and skills with the job requirements. "
            "Analyze both the applicant's background and the job details to:\n"
            "1. Prioritize relevant experiences and skills that match the job requirements\n"
            "2. Use industry-specific keywords from the job description\n"
            "3. Quantify achievements where possible\n"
            "4. Adapt the professional summary to highlight alignment with the role\n"
            "5. Customize skill sections to emphasize relevant competencies\n\n"
            "Below is a LaTeX resume template with placeholders, followed by JSON representations of "
            "applicant data and application data. Generate a strategically formatted LaTeX resume by "
            "filling in the placeholders with appropriate data from the JSON, ensuring the content "
            "is optimized for this specific job application.\n\n"
            "LaTeX Template:\n"
            "-------------------\n"
            f"{self.template}\n"
            "-------------------\n\n"
            "Applicant Data (JSON):\n"
            "-------------------\n"
            f"{applicant_json}\n"
            "-------------------\n\n"
            "Application Data (JSON):\n"
            "-------------------\n"
            f"{application_json}\n"
            "-------------------\n\n"
            "Requirements:\n"
            "- Create compelling bullet points that demonstrate relevant impact and achievements\n"
            "- Incorporate keywords and phrases from the job description naturally\n"
            "- Prioritize experiences that best match the role's requirements\n"
            "- Adjust formatting and section emphasis based on role importance\n"
            "- Do not fabricate any information; use only the provided data\n"
            "- Ensure all LaTeX special characters ('\\', '{', '}', '%') are properly escaped with a backslash\n"
            "- Output only the final, compilation-ready LaTeX code without additional comments\n\n"
        )

        try:
            preview_resume = self.llm_provider.complete(prompt)
        except Exception as e:
            print(f"Error during LLM API call: {e}")
            raise LLMCallFailedException("Error during LLM API call.") from e

        return preview_resume
