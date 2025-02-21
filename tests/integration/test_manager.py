import os
import pytest
from pathlib import Path

# Adjust the import to where your LocalCoordinatingManager is defined.
from src.interface.manager import LocalCoordinatingManager

pytestmark = pytest.mark.skipif(
    os.environ.get("OPENAI_API_KEY") is None,
    reason="Integration test requires a valid OpenAI API key."
)

def test_run_integration(tmp_path: Path, application_raw_text, applicant_resume_txt, applicant_custom_txt):
    """
    Integration test for the LocalCoordinatingManager's run() method.
    It writes the application and applicant data to temporary files,
    runs the resume generation process, and verifies that a valid PDF is generated.
    """
    # Create temporary files for the input texts.
    application_text_path = tmp_path / "application.txt"
    applicant_resume_path = tmp_path / "applicant_resume.txt"
    applicant_custom_path = tmp_path / "applicant_custom.txt"

    application_text_path.write_text(application_raw_text)
    applicant_resume_path.write_text(applicant_resume_txt)
    applicant_custom_path.write_text(applicant_custom_txt)

    # Define an output PDF file path.
    output_pdf_path = str(tmp_path / "output_resume.pdf")

    # Create an instance of the LocalCoordinatingManager.
    manager = LocalCoordinatingManager()

    # Call the run() method.
    manager.run(
        applicant_paths=[str(applicant_resume_path), str(applicant_custom_path)],
        application_path=str(application_text_path),
        output_path=output_pdf_path
    )

    # Verify that the output PDF file is created.
    output_pdf = Path(output_pdf_path)
    assert output_pdf.exists(), "The output PDF was not created."

    # Verify that the file starts with the PDF header "%PDF-"
    with open(output_pdf, "rb") as f:
        header = f.read(5)
    assert header == b"%PDF-", "The generated file does not appear to be a valid PDF."

    print("Integration test passed. PDF generated at:", output_pdf_path)
