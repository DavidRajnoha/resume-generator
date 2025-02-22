from src.modules.pdf_generator.latex_to_pdf import generate_pdf as generate_pdf_func

def generate_pdf(resume_latex: str, output_path: str):
    generate_pdf_func(resume_latex, output_path)
