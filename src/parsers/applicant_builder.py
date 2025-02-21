import json
from abc import ABC

from jsonschema import validate, ValidationError
from src.models.applicant_profile import ApplicantProfile

class AbstractApplicantProfileBuilder(ABC):
    def add_source(self, source_name: str, raw_text: str):
        raise NotImplementedError

    def build(self) -> dict:
        raise NotImplementedError


class ApplicantProfileBuilder(AbstractApplicantProfileBuilder):
    """
    Builder class to accumulate raw text from multiple sources and compose them into
    a JSON representation of the applicant profile using an LLM provider.
    """
    # TODO: Generate the schema out of the ApplicantProfile dataclass
    APPLICANT_PROFILE_SCHEMA = {
        "type": "object",
        "properties": {
            "personal_info": {
                "type": "object",
                "properties": {
                    "full_name": {"type": "string"},
                    "address": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "linkedin": {"type": "string"},
                    "website": {"type": "string"}
                },
                "required": ["full_name", "email"]
            },
            "professional_summary": {"type": "string"},
            "skills": {
                "type": "array",
                "items": {"type": "string"}
            },
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "institution": {"type": "string"},
                        "degree": {"type": "string"},
                        "field_of_study": {"type": "string"},
                        "start_date": {"type": ["string", "null"]},
                        "end_date": {"type": ["string", "null"]},
                        "description": {"type": "string"}
                    },
                    "required": ["institution", "degree"]
                }
            },
            "work_experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "company": {"type": "string"},
                        "location": {"type": "string"},
                        "start_date": {"type": ["string", "null"]},
                        "end_date": {"type": ["string", "null"]},
                        "responsibilities": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["title", "company"]
                }
            },
            "volunteer_experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string"},
                        "organization": {"type": "string"},
                        "location": {"type": "string"},
                        "start_date": {"type": ["string", "null"]},
                        "end_date": {"type": ["string", "null"]},
                        "responsibilities": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["role", "organization"]
                }
            },
            "projects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "role": {"type": "string"},
                        "technologies": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "link": {"type": "string"}
                    },
                    "required": ["name"]
                }
            },
            "certifications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "issuing_organization": {"type": "string"},
                        "issue_date": {"type": ["string", "null"]},
                        "expiration_date": {"type": ["string", "null"]},
                        "credential_id": {"type": "string"},
                        "credential_url": {"type": "string"}
                    },
                    "required": ["name", "issuing_organization"]
                }
            },
            "awards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "issuer": {"type": "string"},
                        "date": {"type": ["string", "null"]},
                        "description": {"type": "string"}
                    },
                    "required": ["title", "issuer"]
                }
            },
            "languages": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "language": {"type": "string"},
                        "proficiency": {"type": "string"}
                    },
                    "required": ["language", "proficiency"]
                }
            },
            "publications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "publisher": {"type": "string"},
                        "publication_date": {"type": ["string", "null"]},
                        "url": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["title", "publisher"]
                }
            },
            "interests": {
                "type": "array",
                "items": {"type": "string"}
            },
            "cover_letter_stories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["title", "content"]
                }
            }
        },
        "required": [
            "personal_info", "professional_summary", "skills",
            "education", "work_experience"
        ]
    }

    def __init__(self, llm_provider):
        """
        :param llm_provider: An object implementing a complete(prompt: str) -> str method.
        """
        self.llm_provider = llm_provider
        self.sources = {}  # Dictionary mapping source names to raw string data.

    def add_source(self, source_name: str, raw_text: str):
        """
        Add a raw text source with a given name.

        :param source_name: Identifier for the data source.
        :param raw_text: Raw text data from that source.
        :return: Self, to allow method chaining.
        """
        self.sources[source_name] = raw_text
        return self

    def build(self) -> dict:
        """
        Combine the accumulated raw sources and call the LLM provider to produce a JSON object.
        Validates that the JSON conforms to the ApplicantProfile schema.

        :return: The parsed JSON as a Python dictionary.
        :raises ValueError: if the JSON output is invalid or does not conform to the schema.
        """
        # Combine all sources into one string with clear separators.
        combined_sources = "\n\n".join(
            [f"{key}:\n{value}" for key, value in self.sources.items()]
        )

        prompt = (
            "You are an application parser that produces a JSON output. Given the following raw text "
            "sources, please generate a JSON object that exactly follows the schema below for an applicant profile.\n\n"
            f"{json.dumps(self.APPLICANT_PROFILE_SCHEMA)}\n\n"
            "Merge and transform the information from the sources as best as possible. Do not include any fields "
            "not mentioned in the schema. Here are the sources:\n"
            "--------------------\n"
            f"{combined_sources}\n"
            "--------------------\n"
            "Output only the JSON object."
        )

        json_response = self.llm_provider.complete(prompt)

        try:
            parsed_json = json.loads(json_response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from LLM output: {e}\nOutput was: {json_response}")

        try:
            return ApplicantProfile.from_json(parsed_json)
        except Exception as e:
            raise ValueError(f"Failed to convert JSON to ApplicantProfile: {e}\nJSON Output: {json_response}")
