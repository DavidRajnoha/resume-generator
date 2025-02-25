import json
from src.modules.cover_letter_builder.cover_letter_builder import CoverLetterBuilder, \
    LLMCallFailedException  # Adjust import based on your project structure


# A dummy LLM provider that implements the complete() method.
class DummyLLMProvider:
    def complete(self, prompt: str) -> str:
        # For testing purposes, simply return a fixed string.
        return "FINAL_COVER_LETTER"


# Dummy applicant data that provides a to_json() method.
class DummyApplicant:
    def to_json(self) -> str:
        return json.dumps({"full_name": "Test Applicant"}, indent=2)


# Dummy application data that provides a to_json() method.
class DummyApplication:
    def to_json(self) -> str:
        return json.dumps({"job_title": "Test Job"}, indent=2)


class DummyLLMProvider404:
    def complete(self, prompt: str) -> str:
        raise Exception("Model not found.")


def test_build_cover_letter(tmp_path):
    # Create a temporary LaTeX template file.
    template_content = "This is a LaTeX template with [PLACEHOLDER]."
    template_file = tmp_path / "cover_letter_template.tex"
    template_file.write_text(template_content)

    # Instantiate dummy data and the dummy LLM provider.
    applicant_data = DummyApplicant()
    application_data = DummyApplication()
    dummy_llm_provider = DummyLLMProvider()

    # Instantiate the CoverLetterBuilder with the temporary template.
    builder = CoverLetterBuilder(applicant_data, application_data, dummy_llm_provider,
                                 str(template_file))

    # Call build_cover_letter and verify that it returns the expected output.
    final_cover_letter = builder.build_cover_letter()
    assert final_cover_letter == "FINAL_COVER_LETTER"


def test_cover_letter_llm_404():
    # Instantiate the CoverLetterBuilder with the dummy LLM provider.
    builder = CoverLetterBuilder(None, None, DummyLLMProvider404())

    # Call build_cover_letter and verify that it raises LLMCallFailedException.
    try:
        builder.build_cover_letter()
    except LLMCallFailedException as e:
        assert str(e) == "Error during LLM API call."
    else:
        assert False, "Expected LLMCallFailedException was not raised."


def test_get_json_with_to_json_method():
    # Test the _get_json method with an object that has to_json.
    builder = CoverLetterBuilder(None, None, None)
    applicant = DummyApplicant()

    result = builder._get_json(applicant)
    expected = json.dumps({"full_name": "Test Applicant"}, indent=2)

    assert result == expected


def test_get_json_without_to_json_method():
    # Test the _get_json method with a plain dict.
    builder = CoverLetterBuilder(None, None, None)
    data = {"job_title": "Software Engineer"}

    result = builder._get_json(data)
    expected = json.dumps(data, indent=2)

    assert result == expected