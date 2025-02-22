# test_applicant_repository_adapter.py

import pytest
from src.persistance.adapters.applicant_repository_adapter import ApplicantRepositoryAdapter

def test_get_existing_applicant_when_none(mock_applicant_repository):
    repo = mock_applicant_repository
    adapter = ApplicantRepositoryAdapter(repo)
    applicant_id = "test1"
    existing = adapter.get_existing_applicant(applicant_id)
    assert existing == (None, None)

def test_merge_raw_texts_without_existing(mock_applicant_repository):
    repo = mock_applicant_repository
    adapter = ApplicantRepositoryAdapter(repo)
    applicant_id = "test2"
    new_text = "Hello"
    merged = adapter.merge_raw_texts(applicant_id, new_text)
    assert merged == "Hello"

def test_merge_raw_texts_with_existing(mock_applicant_repository,
                                       mock_applicant_profile):
    repo = mock_applicant_repository
    applicant_id = "test3"
    # Pre-store a dummy applicant with some raw text.
    dummy_profile = mock_applicant_profile("Hello")
    repo.store_applicant(applicant_id, "Hello", dummy_profile)
    adapter = ApplicantRepositoryAdapter(repo)
    merged = adapter.merge_raw_texts(applicant_id, " World")
    assert merged == "Hello World"

def test_fetch_applicant_or_fail(mock_applicant_repository,
                                 mock_applicant_profile):
    repo = mock_applicant_repository
    adapter = ApplicantRepositoryAdapter(repo)
    applicant_id = "test4"
    # When not present, should raise ValueError.
    with pytest.raises(ValueError):
        adapter.fetch_applicant_or_fail(applicant_id)
    # Now store and try fetching.
    dummy_profile = mock_applicant_profile("TestData")
    repo.store_applicant(applicant_id, "TestData", dummy_profile)
    fetched = adapter.fetch_applicant_or_fail(applicant_id)
    assert fetched == dummy_profile
