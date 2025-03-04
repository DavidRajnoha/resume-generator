import os
import glob
from typing import List, Optional

from src.modules.applicant_loader import load_applicant_data
from src.modules.application_loader import load_application_data
from src.modules.applicant_parser_module import ApplicantParserModule
from src.modules.application_parser_module import ApplicationParserModule
from src.modules.resume_builder_module import ResumeBuilderModule
from src.modules.cover_letter_builder_module import CoverLetterBuilderModule
from src.modules.pdf_generator_module import generate_pdf
from src.models.applicant_profile import ApplicantProfile


class Coordinator:
    def __init__(self, applicant_id: str, applicant_paths: List[str],
                 applications_dir: str, output_dir: str,
                 applicant_parser=None, application_parser=None,
                 resume_builder=None, cover_letter_builder=None):
        self.applicant_parser = applicant_parser or ApplicantParserModule()
        self.application_parser = application_parser or ApplicationParserModule()
        self.resume_builder = resume_builder or ResumeBuilderModule()
        self.cover_letter_builder = cover_letter_builder or CoverLetterBuilderModule()

        self.applicant_id = applicant_id
        self.applicant_paths = applicant_paths
        self.applications_dir = applications_dir
        self.output_dir = output_dir
        self.applicant: Optional[ApplicantProfile] = None

    def orchestrate_applicant_data(self):
        # Load applicant texts and parse the applicant profile.
        applicant_texts = load_applicant_data(self.applicant_paths)
        self.applicant = self.applicant_parser.parse(self.applicant_id, applicant_texts)
        print(f"Loaded and parsed data for applicant {self.applicant_id}")

    def get_application_files(self) -> List[str]:
        # Retrieve all files (recursively) from the applications directory.
        return glob.glob(os.path.join(self.applications_dir, "**"), recursive=True)

    def orchestrate_application(self, application_path: str) -> bool:
        try:
            # Derive a base name from the application file.
            application_name = os.path.splitext(os.path.basename(application_path))[0]

            # Load and parse application data.
            application_text = load_application_data(application_path)
            application = self.application_parser.parse(application_text)

            # Build resume and cover letter content.
            # resume_tex = self.resume_builder.build(self.applicant, application)
            cover_tex = self.cover_letter_builder.build(self.applicant, application)

            # Define output file paths.
            # resume_output_path = os.path.join(self.output_dir, f"{application_name}_resume.pdf")
            cover_output_path = os.path.join(self.output_dir, f"{application_name}_cover_letter.pdf")

            # Generate PDFs.
            # generate_pdf(resume_tex, resume_output_path)
            generate_pdf(cover_tex, cover_output_path)

            print(f"Processed application {application_name}")
            return True

        except Exception as e:
            print(f"Error processing {application_path}: {e}")
            return False

    def run(self):
        # Orchestrate the entire pipeline.
        self.orchestrate_applicant_data()

        application_files = self.get_application_files()
        if not application_files:
            print(f"No application files found in {self.applications_dir}")
            return

        print(f"Found {len(application_files)} application files")
        success_count = 0
        for file in application_files:
            if os.path.isfile(file):  # Only process files.
                if self.orchestrate_application(file):
                    success_count += 1

        print(f"Completed: {success_count} applications processed out of {len(application_files)}")
