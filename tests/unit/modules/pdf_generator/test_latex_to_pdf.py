from src.modules.pdf_generator.latex_to_pdf import generate_pdf


def test_generate_pdf(tmp_path):
    # Create a valid simple latex template.
    template_content = r"""
    \documentclass{article}
    \begin{document}
    Hello, this is a simple LaTeX document.
    \end{document}
    """

    # Define the output PDF path.
    output_pdf = tmp_path / "resume.pdf"

    generate_pdf(template_content, str(output_pdf))

    # Verify that the PDF file exists.
    assert output_pdf.exists(), "The PDF file was not created."

    # Check that the PDF file starts with the standard PDF header '%PDF-'.
    with open(output_pdf, "rb") as f:
        header = f.read(5)
    assert header == b"%PDF-", "The generated file does not appear to be a valid PDF."