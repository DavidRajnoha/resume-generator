import pytest
from typing import List


def test_load_applicant_data(strategy):
    paths: List[str] = ["file1.txt", "file2.txt"]
    result = strategy.load_applicant_data(paths, retry=2)
    # Expect each element to be "Dummy content from <path>"
    assert result == [f"Dummy content from {p}" for p in paths]

def test_load_application_data(strategy):
    path = "application.txt"
    result = strategy.load_application_data(path, retry=3)
    assert result == f"Dummy content from {path}"

def test_parse_application_data(strategy):
    # We simulate the parsing process by checking that the dummy llm_provider is used.
    # For our test, we'll pass a simple application text.
    application_text = "Test application text"
    # We assume PlainTextParser(llm_provider).parse returns something we can check.
    # Since we don't override that here, we check that no exception is raised.
    result = strategy.parse_application_data(application_text, retry=1)
    # Without a full dummy implementation of ApplicationData,
    # we at least assert that some non-empty result is returned.
    assert result is not None

def test_parse_applicant_data(strategy):
    # We need to provide at least two texts.
    applicant_texts = ["Test resume text", "Test custom text"]
    result = strategy.parse_applicant_data(applicant_texts, retry=1)
    # Without a full dummy implementation, assert that result is not None.
    assert result is not None

# def test_build_resume(strategy):
#     # For building a resume, we simulate applicant and application data.
#     # In a real test you would use actual instances of ApplicantProfile and ApplicationData.
#     # Here, we'll simply pass dummy objects.
#     dummy_applicant = DummyApplicantProfile()
#     dummy_application = DummyApplicationData()
#     result = strategy.build_resume(dummy_applicant, dummy_application, retry=2)
#     # According to the implementation, the resume builder should return some LaTeX string.
#     # Here, we simply check that the result is a non-empty string.
#     assert isinstance(result, str)
#     assert result.strip() != ""

def test_generate_pdf(strategy, capsys):
    # Call generate_pdf with dummy resume_latex and output_path.
    dummy_latex = "Dummy LaTeX content"
    output_path = "output.pdf"
    strategy.generate_pdf(dummy_latex, output_path, retry=1)
    # Capture the printed output to verify our dummy_generate_pdf was called.
    captured = capsys.readouterr().out
    assert f"Dummy PDF generated at {output_path}" in captured
