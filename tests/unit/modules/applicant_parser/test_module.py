# test_applicant_parser_module.py

from src.modules.applicant_parser_module import ApplicantParserModule

def test_parse_new_applicant(mock_applicant_repository,
                             mock_applicant_profile_builder):

    module = ApplicantParserModule(builder=mock_applicant_profile_builder,
                                   repository=mock_applicant_repository)
    applicant_id = "user1"
    texts = ["Hello", " ", "World"]
    profile = module.parse(applicant_id, texts)
    # The DummyApplicantProfile should have raw_text "Hello World"
    assert profile.raw_text == "Hello World"
    # Verify that the repository now stores the data.
    stored = mock_applicant_repository.get_applicant(applicant_id)
    assert stored is not None
    assert stored[0] == "Hello World"
    assert stored[1] == profile

def test_parse_existing_applicant_when_no_new_texts(mock_applicant_repository,
                             mock_applicant_profile_builder):

    module = ApplicantParserModule(builder=mock_applicant_profile_builder,
                                   repository=mock_applicant_repository)
    applicant_id = "user2"
    # First, create an applicant profile.
    texts = ["Data", "Test"]
    profile1 = module.parse(applicant_id, texts)
    # Now, calling with no new texts should fetch the stored applicant.
    profile2 = module.parse(applicant_id, [])
    # They should be equal.
    assert profile2 == profile1
