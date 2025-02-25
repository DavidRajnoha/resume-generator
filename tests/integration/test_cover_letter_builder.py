import os
import pytest
from pathlib import Path
from src.modules.cover_letter_builder.cover_letter_builder import CoverLetterBuilder
from src.llm_wrappers.llm_providers import OpenAILLMProvider
from src.modules.pdf_generator.latex_to_pdf import generate_pdf

# Skip the integration test if no API key is provided.
pytestmark = pytest.mark.skipif(
    os.environ.get("OPENAI_API_KEY") is None,
    reason="Integration test requires OpenAI API key."
)


def test_cover_letter_builder_and_pdf_generation(tmp_path: Path, applicant, application, model):
    llm_provider = OpenAILLMProvider(model=model, temperature=0.3, max_tokens=1500)

    builder = CoverLetterBuilder(applicant, application, llm_provider)
    final_latex = builder.build_cover_letter()

    assert isinstance(final_latex, str) and len(final_latex) > 0, "Final LaTeX cover letter is empty."
    print(final_latex)

    output_pdf_path = str(tmp_path / "cover_letter_output.pdf")
    generate_pdf(final_latex, output_pdf_path)

    assert os.path.exists(output_pdf_path), "PDF file was not generated."

    # Verify the PDF file starts with the standard header "%PDF-".
    with open(output_pdf_path, "rb") as pdf_file:
        header = pdf_file.read(5)
    assert header == b"%PDF-", "The generated file does not appear to be a valid PDF."

    print(f"PDF file generated at: {output_pdf_path}")
