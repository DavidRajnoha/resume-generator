#!/usr/bin/env python
# File: cli.py

import argparse
from src.coordination.coordination_pipeline import ResumePipeline  # Adjust import if needed

def main():
    parser = argparse.ArgumentParser(description="Resume Generation Pipeline CLI")
    parser.add_argument("--applicant-id", type=str, required=True,
                        help="Unique identifier for the applicant.")
    parser.add_argument("--applicant-paths", nargs="+", required=True,
                        help="File paths to applicant texts (one or more).")
    parser.add_argument("--application-path", type=str, required=True,
                        help="File path to the application text.")
    parser.add_argument("--output-path", type=str, required=True,
                        help="File path where the generated PDF should be saved.")

    args = parser.parse_args()


    # Create the pipeline instance using the provided arguments.
    pipeline = ResumePipeline(
        applicant_id=args.applicant_id,
        applicant_paths=args.applicant_paths,
        application_path=args.application_path,
        output_path=args.output_path
    )

    # Run the pipeline.
    pipeline.run()

if __name__ == "__main__":
    main()
