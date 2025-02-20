import json
import os

from src.models.applicant_profile import ApplicantProfile


class LLMCallFailedException(Exception):
    pass

class ResumeBuilder:
    def __init__(self, applicant_data: ApplicantProfile, application_data: ApplicantProfile, llm_provider,
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
            "You are a resume builder that produces valid LaTeX output. "
            "Below is a LaTeX resume template with placeholders followed by JSON representations of "
            "applicant data and application data. Please generate a personalized, well-formatted "
            "LaTeX resume by filling in the placeholders with the appropriate data from the JSON. "
            "Ensure that no placeholders remain in the final output and that the document is ready for compilation.\n\n"
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
            "Escape the LaTeX special characters like '\\', '{', '}', and '%' with a backslash. "
            "Please output the final LaTeX code for the resume."
        )

        try:
            final_resume = self.llm_provider.complete(prompt)
            return final_resume
        except Exception as e:
            print(f"Error during LLM API call: {e}")
            raise LLMCallFailedException("Error during LLM API call.") from e
