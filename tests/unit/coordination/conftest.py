import pytest

from src.coordination.coordination_strategy import LocalCoordinationStrategy
from src.llm_wrappers.llm_providers import LLMProvider
from src.parsers.applicant_builder import AbstractApplicantProfileBuilder
from src.parsers.application_parser import ApplicationParser


class DummyApplicantProfile:
    def __init__(self, name="Dummy Applicant"):
        self.name = name

class DummyApplicationData:
    def __init__(self, content="Dummy Application"):
        self.content = content

class DummyLLMProvider(LLMProvider):
    def complete(self, prompt: str) -> str:
        return "DUMMY RESPONSE"


class DummyApplicationParser(ApplicationParser):
    def parse(self, text: str):
        return DummyApplicationData()

class DummyApplicantProfileBuilder(AbstractApplicantProfileBuilder):
    def add_source(self, source_name: str, raw_text: str):
        return self

    def build(self):
        return DummyApplicantProfile()


# We also override generate_pdf to simply record that it was called.
def dummy_generate_pdf(resume_latex: str, output_path: str):
    print(f"Dummy PDF generated at {output_path}")

# Define a dummy load_text that doesn't read from the file system.
def dummy_load_text(path: str) -> str:
    return f"Dummy content from {path}"

@pytest.fixture
def llm_provider():
    return DummyLLMProvider()


@pytest.fixture
def dummy_application_parser():
    return DummyApplicationParser()

@pytest.fixture
def dummy_applicant_builder():
    return DummyApplicantProfileBuilder()


@pytest.fixture
def strategy(monkeypatch, llm_provider, dummy_application_parser, dummy_applicant_builder):
    strat = LocalCoordinationStrategy(llm_provider, dummy_application_parser, dummy_applicant_builder)
    # Monkey-patch the static load_text method to avoid file I/O.
    monkeypatch.setattr(LocalCoordinationStrategy, "load_text", dummy_load_text)
    # Monkey-patch generate_pdf function used by the strategy.
    monkeypatch.setattr(strat, "generate_pdf", lambda latex, output, retry=1: dummy_generate_pdf(latex, output))
    return strat