import pytest

from src.persistance.applicant_repository import ApplicantRepository

class MockApplicantProfile:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def __eq__(self, other):
        if not isinstance(other, MockApplicantProfile):
            return False
        return self.raw_text == other.raw_text

    def __repr__(self):
        return f"DummyApplicantProfile({self.raw_text!r})"


class MockApplicantRepository(ApplicantRepository):
    """
    A simple in-memory repository that mimics the ApplicantRepository interface.
    Stores data in a dict mapping applicant_id to (raw_text, applicant_profile).
    """
    def __init__(self):
        self.storage = {}

    def get_applicant(self, applicant_id: str):
        return self.storage.get(applicant_id)

    def store_applicant(self, applicant_id: str, raw_text: str, applicant_profile):
        self.storage[applicant_id] = (raw_text, applicant_profile)


class MockApplicantProfileBuilder:
    """
    A fake builder that records the raw text it is given and, when build() is called,
    returns a DummyApplicantProfile with the combined text.
    """
    def __init__(self):
        self.sources = {}

    def add_source(self, label: str, raw_text: str):
        self.sources[label] = raw_text
        return self

    def build(self):
        combined = "".join(self.sources.values())
        # Reset the builder state after building
        self.sources = {}
        return MockApplicantProfile(combined)


@pytest.fixture
def mock_applicant_repository():
    return MockApplicantRepository()

@pytest.fixture
def mock_applicant_profile_builder():
    return MockApplicantProfileBuilder()

@pytest.fixture
def mock_applicant_profile():
    def _mock_applicant_profile(raw_text: str):
        return MockApplicantProfile(raw_text)
    return _mock_applicant_profile