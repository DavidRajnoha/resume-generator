import json
import os

from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData


class LLMCallFailedException(Exception):
    pass


class CoverLetterBuilder:
    def __init__(self, applicant_data: ApplicantProfile, application_data: ApplicationData, llm_provider,
                 template_path=None):
        """
        :param applicant_data: An object or dict containing applicant data.
                               If an object, it should implement a to_json() method.
        :param application_data: An object or dict containing application/job data.
                                 If an object, it should implement a to_json() method.
        :param llm_provider: Provider for the language model service.
        :param template_path: Path to the LaTeX cover letter template with placeholders.
        """
        if template_path is None:
            source_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(source_dir, "templates", "cover_letter_template.tex")

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

    def build_cover_letter(self) -> str:
        """
        Build a personalized cover letter by providing the raw LaTeX template and JSON data
        to the LLM. The LLM is instructed to merge the two and output a final,
        fully populated, valid LaTeX cover letter.

        :return: A string containing the final LaTeX cover letter.
        """
        applicant_json = self._get_json(self.applicant_data)
        application_json = self._get_json(self.application_data)

        prompt = (
            "You are a cover letter builder that produces valid LaTeX output. "
            "Below is a LaTeX cover letter template with placeholders followed by JSON representations of "
            "applicant data and application data. Please generate a personalized, well-formatted "
            "LaTeX cover letter by filling in the placeholders with the appropriate data from the JSON. "

            "The cover letter should follow this specific style and structure:\n"
            "1. Begin with a direct, specific statement of interest in the exact position\n"
            "2. Explain why you're interested in this specific role or project, showing you've researched it\n"
            "3. Connect your academic background to the position requirements\n"
            "4. Highlight relevant experiences that directly relate to the job description\n"
            "5. Address potential gaps in experience positively, emphasizing ability to learn quickly\n"
            "6. Use clear, concise paragraphs that each make a specific point\n"
            "8. Close with enthusiasm about contributing to the company\n"

            "The language style should have these specific characteristics:\n"
            "- Use direct, confident expressions like 'I am writing to express my strong interest' and 'I am particularly excited about'\n"
            "- Create clear connections between the applicant's experience and the role requirements\n"
            "- Incorporate technical terminology relevant to the position to demonstrate domain knowledge\n"
            "- Employ phrases that express genuine enthusiasm such as 'particularly excites me' and 'I am excited about the possibility'\n"
            "- Use forward-looking language like 'contributing to the advancement' and 'expanding my knowledge'\n"
            "- Vary sentence structure, mixing longer explanatory sentences with shorter, more direct statements\n"
            "The overall tone should balance professionalism with genuine enthusiasm, demonstrate specific knowledge of the position, "
            "and convey confidence without presumption. Technical terminology should be used precisely and naturally.\n\n"
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
            "Please output only the final LaTeX code for the cover letter without any additional text or comments. "
            "Ensure that the LaTeX is valid and not missing any properties and will not fail to compile.\n\n"
        )

        try:
            final_cover_letter = self.llm_provider.complete(prompt)
            return final_cover_letter
        except Exception as e:
            print(f"Error during LLM API call: {e}")
            raise LLMCallFailedException("Error during LLM API call.") from e