import json
from src.modules.resume_builder.resume_builder import ResumeBuilder, \
    LLMCallFailedException  # Adjust import based on your project structure


# A dummy LLM provider that implements the complete() method.
class DummyLLMProvider:
    def complete(self, prompt: str) -> str:
        # For testing purposes, simply return a fixed string.
        return "FINAL_RESUME"


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


def test_build_resume(tmp_path):
    # Create a temporary LaTeX template file.
    template_content = "This is a LaTeX template with [PLACEHOLDER]."
    template_file = tmp_path / "template.tex"
    template_file.write_text(template_content)

    # Instantiate dummy data and the dummy LLM provider.
    applicant_data = DummyApplicant()
    application_data = DummyApplication()
    dummy_llm_provider = DummyLLMProvider()

    # Instantiate the ResumeBuilder with the temporary template.
    builder = ResumeBuilder(applicant_data, application_data, dummy_llm_provider)

    # Call build_resume and verify that it returns the expected output.
    final_resume = builder.build_resume()
    assert final_resume == "FINAL_RESUME"

def test_llm_404():
    # Instantiate the ResumeBuilder with the dummy LLM provider.
    builder = ResumeBuilder(None, None, DummyLLMProvider404())

    # Call build_resume and verify that it raises a FileNotFoundError.
    try:
        builder.build_resume()
    except LLMCallFailedException as e:
        assert str(e) == "Error during LLM API call."
    else:
        assert False, "Expected FileNotFoundError was not raised."

