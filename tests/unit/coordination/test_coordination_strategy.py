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
    # Test that parsing application data returns a non-None result.
    application_text = "Test application text"
    result1 = strategy.parse_application_data(application_text, retry=1)
    assert result1 is not None, "Initial application parsing failed; got None."

    # Call again with the same text to test caching.
    result2 = strategy.parse_application_data(application_text, retry=1)
    assert result2 is not None, "Cached application parsing returned None."

    # Assuming equality is defined for ApplicationData, they should be equal.
    assert result1 == result2, "Cached application data should be equal for identical input."


def test_parse_applicant_data(strategy):
    applicant_id = "test_applicant"

    # First, build a new applicant profile with initial texts.
    initial_texts = ["Test resume text", "Test custom text"]
    result1 = strategy.parse_applicant_data(applicant_id, initial_texts, retry=1)
    assert result1 is not None, "Initial applicant parsing failed; got None."

    # Calling with no new texts should return the stored applicant.
    result2 = strategy.parse_applicant_data(applicant_id, [], retry=1)
    assert result2 is not None, "Fetching stored applicant returned None."
    assert result1 == result2, "No new texts provided should return cached applicant data."

    # Now, simulate merging by providing additional texts.
    additional_texts = [" More details."]
    result3 = strategy.parse_applicant_data(applicant_id, additional_texts, retry=1)
    assert result3 is not None, "Applicant merging with additional texts returned None."

    # We expect that merging new texts produces an updated profile,
    # so the result should now differ from the previously stored profile.
    assert result3 != result2, "Merging new texts should produce an updated applicant profile."


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
