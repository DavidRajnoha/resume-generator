import os

import pytest

from src.parsers.application_parser import PlainTextParser


@pytest.fixture
def raw_text():
    return """
    Software Engineer needed at Tech Corp.
    Department: Engineering
    Location: Remote
    Employment Type: Full-Time
    Job Description: Develop and maintain software solutions.
    Responsibilities: Write code, Review code.
    Requirements: Proficiency in Python, Teamwork.
    Posted Date: 2025-02-19
    Closing Date: 2025-03-01

    Cover Letter:
    I am excited to apply for this position.

    Additional Notes:
    Looking forward to contributing to the team.
    """

@pytest.fixture
def raw_text_extended():
    return """
 About the job

An exciting, 10-week, paid, on-site Internship experience awaits! Gain real life experience into the world of Insurance Brokerage. You will work within a high-energy, fast paced environment that is both competitive and fun. This role will afford the opportunity to work on-site in our New York, NY office for Summer 2025. Internship opportunities are within our Property & Casualty or Employee Benefits practices and include opportunities on our Real Estate, Entertainment, Employee Benefits, Private Client and Commercial Lines Teams and others.


Our summer Internship program offers the chance to have practical, real-world experience at a Top 16 P&C Broker. As a part of the program, you will have the opportunity to work on business specific projects where you will gain knowledge and experience to supplement and strengthen your skills.


You will:

    Receive targeted business and technical training with a greater understanding of the Retail Brokerage Insurance industry
    Become acclimated to working in an environment dedicated to exceeding client expectations and delivering products and services distinct to unique client needs
    Work with account and project teams to deliver business-focused initiatives and strategic recommendations
    Be presented with real world business, risk management, and insurance experience and learn to apply the concepts you’ve learned in the classroom through project work
    Shadow team members on meetings with clients and attend client decision meetings and conference calls
    Be assigned a dedicated Internship Mentor & Internship Ambassador during your Internship experience
    Engage weekly with Sr. Leaders across the company on our renowned “Leadership Perspective” Series
    Participate weekly in our “Professional Insights” Series (Creating/Updating Your LinkedIn profile, Interviewing Best Practices, Resume Writing, Job Search tips etc.)
    Be actively involved in our “RiskMate” Peer Program for breakout sessions throughout the summer


Requirements & Qualifications:

    Must be a Rising Senior (Anticipated Graduation 5/26)
    Must be available for entire 10-week program, including an Intern Summit to be held in Boston, MA June 2nd – June 4th (expenses paid)
    3.0 GPA or higher (Transcript required prior to interview)
    Preference for Finance, Risk Management or Economics majors (previous insurance internship experience may be considered in lieu of)
    Must be available to interview in December/January
    Exceptional organizational and time-management skills
    Must be detailed oriented and proficient with MS Office Suite


Risk Strategies is the 9th largest privately held US brokerage firm offering comprehensive risk management advice, insurance and reinsurance placement for Property & Casualty, Employee Benefits, Private Client Services, as well as

consulting services and financial & wealth solutions. With over 200 offices and more than 5,400 employees, Risk Strategies is as part of the Accession Risk Management Group family of companies.


Industry recognition includes being certified a 2024 Rise Elite Internship Program Recipient, Great Place to Work in 2025 and is on the Inc. 5000 list as one of America’s fastest growing private companies.



At Risk Strategies Company, base pay is one part of our total compensation package, which also includes a comprehensive suite of benefits, including medical, dental, vision, disability, and life insurance, retirement savings, and paid time off and paid holidays for eligible employees. The total compensation for a position may also include other elements dependent on the position offered. The expected base pay range for this position is $21/hour.
    """


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"],
    reason="Skipping integration test because OPENAI_API_KEY is not set"
)
def test_parse_with_real_llm(raw_text_extended):
    # Replace with your real LLM provider implementation
    from src.llm_wrappers.llm_providers import OpenAILLMProvider  # Adjust based on your actual provider

    real_llm = OpenAILLMProvider()
    parser = PlainTextParser(real_llm)

    application_data = parser.parse(raw_text_extended)

    assert application_data.position_information.job_title is not None
    assert application_data.company_profile.name is not None
    # assert len(application_data.custom_sections) >= 1
    print(application_data.to_json())  # Optional: Print parsed JSON for debugging
