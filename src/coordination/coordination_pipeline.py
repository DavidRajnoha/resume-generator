from typing import List, Optional
from src.coordination.strategies.local_coordination_strategy import LocalCoordinationStrategy, CoordinationStrategy
from src.coordination.retry_decorator import retry, MAX_RETRIES
from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData


class ResumePipeline:
    def __init__(self, applicant_id: str, applicant_paths: List[str], application_path: str,
                 resume_output_path: str, cover_letter_output_path: str,
                 strategy: Optional[CoordinationStrategy] = None):
        self.applicant_id = applicant_id
        self.applicant_paths = applicant_paths
        self.application_path = application_path
        self.resume_output_path = resume_output_path
        self.cover_letter_output_path = cover_letter_output_path
        self.strategy = strategy or LocalCoordinationStrategy()
        self.applicant_texts: List[str] = []
        self.application_text: Optional[str] = None
        self.applicant: Optional[ApplicantProfile] = None
        self.application: Optional[ApplicationData] = None
        self.resume_latex: Optional[str] = None
        self.cover_latex: Optional[str] = None

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying load_applicant_data...")
    def load_applicant_data(self):
        self.applicant_texts = self.strategy.load_applicant_data(self.applicant_paths)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying load_application_data...")
    def load_application_data(self):
        self.application_text = self.strategy.load_application_data(self.application_path)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying parse_applicant_data...")
    def parse_applicant_data(self):
        self.applicant = self.strategy.parse_applicant_data(self.applicant_id, self.applicant_texts)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying parse_application_data...")
    def parse_application_data(self):
        self.application = self.strategy.parse_application_data(self.application_text)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying build_resume...")
    def build_resume(self):
        self.resume_latex = self.strategy.build_resume(self.applicant, self.application)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying build_cover_letter...")
    def build_cover_letter(self):
        self.cover_latex = self.strategy.build_cover_letter(self.applicant, self.application)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying generate_resume_pdf...")
    def generate_resume_pdf(self):
        self.strategy.generate_pdf(self.resume_latex, self.resume_output_path)

    @retry(max_retries=MAX_RETRIES, retry_message="Retrying generate_cover_letter_pdf...")
    def generate_cover_letter_pdf(self):
        self.strategy.generate_pdf(self.cover_latex, self.cover_letter_output_path)

    def run(self):
        try:
            self.load_applicant_data()
            self.load_application_data()
            self.parse_applicant_data()
            self.parse_application_data()

            # Generate resume
            self.build_resume()
            self.generate_resume_pdf()

            # Generate cover letter
            self.build_cover_letter()
            self.generate_cover_letter_pdf()

            print("Resume and cover letter generation completed successfully.")
        except Exception as e:
            print(f"Pipeline aborted due to error: {e}")