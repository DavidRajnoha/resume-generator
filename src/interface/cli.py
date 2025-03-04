#!/usr/bin/env python
# File: cli.py

import argparse
import os
from src.coordination.coordinator import Coordinator  # Adjust import if needed


def main():
    parser = argparse.ArgumentParser(description="Resume Generation Pipeline CLI")
    parser.add_argument("--applicant-id", type=str, required=True,
                        help="Unique identifier for the applicant.")
    parser.add_argument("--applicant-paths", nargs="+", required=False,
                        help="File paths to applicant texts (one or more).")
    parser.add_argument("--applications-dir", type=str, required=True,
                        help="Directory containing application files to process.")
    parser.add_argument("--output-dir", type=str, required=True,
                        help="Directory where generated PDFs should be saved.")

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Create the pipeline instance using the provided arguments.
    pipeline = Coordinator(
        applicant_id=args.applicant_id,
        applicant_paths=args.applicant_paths if args.applicant_paths else [],
        applications_dir=args.applications_dir,
        output_dir=args.output_dir
    )

    # Run the pipeline.
    pipeline.run()


if __name__ == "__main__":
    main()