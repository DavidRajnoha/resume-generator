import os
import pytest
import json
import subprocess
from pathlib import Path
from src.builders.resume_builder import ResumeBuilder
from src.llm_wrappers.llm_providers import OpenAILLMProvider
from src.utils.latex_to_pdf import generate_pdf # Ensure this provider is implemented.

# Skip the integration test if no API key is provided.
pytestmark = pytest.mark.skipif(
    os.environ.get("OPENAI_API_KEY") is None,
    reason="Integration test requires OpenAI API key."
)

def test_resume_builder_and_pdf_generation(tmp_path: Path, applicant, application, model):
    llm_provider = OpenAILLMProvider(model=model, temperature=0.3, max_tokens=1500)

    builder = ResumeBuilder(applicant, application, llm_provider)
    final_latex = builder.build_resume()

    assert isinstance(final_latex, str) and len(final_latex) > 0, "Final LaTeX resume is empty."
    print(final_latex)

    output_pdf_path = str(tmp_path / "resume_output.pdf")
    generate_pdf(final_latex, output_pdf_path)

    assert os.path.exists(output_pdf_path), "PDF file was not generated."

    # Verify the PDF file starts with the standard header "%PDF-".
    with open(output_pdf_path, "rb") as pdf_file:
        header = pdf_file.read(5)
    assert header == b"%PDF-", "The generated file does not appear to be a valid PDF."

    print(f"PDF file generated at: {output_pdf_path}")
