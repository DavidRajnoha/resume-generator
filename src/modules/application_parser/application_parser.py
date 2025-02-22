import json
from abc import abstractmethod
from src.llm_wrappers.llm_providers import LLMProvider
from src.models.application_data import ApplicationData

class ApplicationParser:
    @abstractmethod
    def parse(self, text: str) -> ApplicationData:
        """
        Given a plain text input, parse and return the structured ApplicationData object.
        """
        pass


class PlainTextParser(ApplicationParser):
    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.prompt = """
You are an assistant tasked with converting raw application text into structured JSON data.
The JSON object must conform exactly to the following schema:

{
  "position_information": {
      "job_title": string,            // The title of the job.
      "department": string,           // The department the job belongs to.
      "location": string,             // The location of the job.
      "employment_type": string,      // e.g., "Full-Time", "Part-Time", "Contract".
      "description": string,          // A description of the job.
      "responsibilities": [string],   // A list of job responsibilities.
      "requirements": [string],       // A list of job requirements.
      "posted_date": string (optional),   // The date the job was posted.
      "closing_date": string (optional)   // The date the application closes.
  },
  "company_profile": {
      "name": string,               // The company's name.
      "website": string,            // The company's website.
      "description": string,        // A description of the company.
      "industry": string,           // The company's industry.
      "size": string                // Company size, e.g., "50-200 employees" or "Startup".
  },
  "custom_sections": [
      {
          "section_title": string,  // The title of the custom section (e.g., cover letter).
          "content": string         // The content of this section.
      }
  ],
  "extra_text": [string]           // An array of additional plain text strings, if any.
}

Given the raw text input, extract the relevant information and output a valid JSON object strictly following this schema.
Ensure that your response contains only the JSON object with no additional commentary or formatting.
"""

    def parse(self, text: str) -> ApplicationData:
        full_prompt = self.prompt.strip() + "\n\n" + text.strip()
        application_json_str = self.llm.complete(full_prompt)
        try:
            application_json = json.loads(application_json_str)
        except json.JSONDecodeError:
            # TODO: Implement retry logic or error handling
            raise ValueError("The generated JSON is invalid.")

        return ApplicationData.from_json(application_json)