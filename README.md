
# Resume Generator

A modular pipeline for generating customized resumes from applicant and application data. The system is designed to run locally via a CLI, with future plans for AWS Lambda deployment and a web interface.

## Features

- **Modular Design:**  
  Separate components for data loading, parsing, resume building, and PDF generation.
- **Flexible Coordination:**  
  A unified coordination strategy abstracts the underlying module calls.
- **Extensible Storage:**  
  Repository adapters enable easy swapping between file storage and other solutions (e.g., a vector database).
- **Local CLI Interface:**  
  Run the entire pipeline from the command line for local testing.

## Project Structure

```
resume_generator/
├── src/
│   ├── __init__.py
│   ├── coordination/
│   │   ├── coordination_pipeline.py
│   │   ├── coordination_strategy.py
│   │   ├── retry_decorator.py
│   │   └── strategies/
│   │       └── local_coordination_strategy.py
│   ├── interface/
│   │   ├── __init__.py
│   │   └── cli.py         # CLI entry point
│   ├── llm_wrappers/
│   │   ├── __init__.py
│   │   └── llm_providers.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── applicant_profile.py
│   │   └── application_data.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── applicant_loader.py
│   │   ├── applicant_parser_module.py
│   │   ├── application_loader.py
│   │   ├── application_parser_module.py
│   │   ├── pdf_generator_module.py
│   │   └── resume_builder_module.py
│   ├── persistance/
│   │   ├── __init__.py
│   │   ├── applicant_repository.py
│   │   ├── application_repository.py
│   │   ├── file_storage/
│   │   │   ├── __init__.py
│   │   │   ├── file_applicant_repository.py
│   │   │   └── file_application_repository.py
│   │   └── adapters/
│   │       ├── __init__.py
│   │       └── applicant_repository_adapter.py
├── tests/                   # Unit and integration tests
├── pyproject.toml           # Poetry configuration & entry points
├── poetry.lock
└── README.md
```

## Installation

This project uses [Poetry](https://python-poetry.org/):

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/resume_generator.git
   cd resume_generator
   ```

2. **Install dependencies:**

   ```bash
   poetry install
   ```

## Usage

### CLI

A CLI is provided for local execution. After installation, run:

```bash
poetry run resume-cli --applicant-id user123 --applicant-paths resume.txt custom.txt --application-path app.txt --output-path resume.pdf
```

This command loads the applicant and application data, parses them, builds a resume, and generates a PDF at the specified output path.

## Future Directions

- **AWS Lambda Deployment:**  
  Implement an AWSCoordinationStrategy that invokes Lambda functions or REST endpoints.
- **Advanced Storage:**  
  Swap file storage with a vector database or another storage solution using repository adapters.
- **LORA model:**  
  Implement a LORA model for generating resumes from applicant and application data.

## Running Tests

Run all tests with:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License.

