import json

import pytest

from src.models.applicant_profile import ApplicantProfile
from src.models.application_data import ApplicationData


@pytest.fixture
def applicant_id():
    return "alex_johnson"

@pytest.fixture
def applicant(applicant_data_json):
    return ApplicantProfile.from_json(applicant_data_json)


@pytest.fixture
def application(application_data_json):
    return ApplicationData.from_json(application_data_json)


@pytest.fixture
def applicant_data_json():
    return {
        "personal_info": {
    "full_name": "Alex Johnson",
    "address": "",
    "phone": "+1 555 123-4567",
    "email": "alex.johnson@example.com",
    "linkedin": "linkedin.com/in/alex-johnson-123456",
    "website": "github.com/alexjohnson"
  },
  "professional_summary": "Alex Johnson is a dedicated Software Engineer specializing in full-stack development and artificial intelligence. With over 2 years of experience, he has a proven track record of building robust web applications and AI models. Alex is passionate about leveraging technology to solve real-world problems and is always eager to learn and adopt new technologies.",
  "skills": [
    "JavaScript",
    "React",
    "Python",
    "Django",
    "Go",
    "TensorFlow",
    "Docker",
    "Kubernetes",
    "AWS",
    "Agile Methodologies",
    "Team Leadership"
  ],
  "education": [
    {
      "institution": "Tech University",
      "degree": "B.S. in Computer Science",
      "field_of_study": "Computer Science",
      "start_date": None,
      "end_date": "2023",
      "description": None
    },
    {
      "institution": "Innovation University",
      "degree": "M.S. in Artificial Intelligence",
      "field_of_study": "Artificial Intelligence",
      "start_date": "2023",
      "end_date": "2025",
      "description": None
    }
  ],
  "work_experience": [
    {
      "title": "Software Developer",
      "company": "Web Solutions Inc.",
      "location": None,
      "start_date": "2023",
      "end_date": "Present",
      "responsibilities": [
        "Developed and maintained web applications using React and Django, improving client satisfaction by 25%",
        "Collaborated with cross-functional teams to deliver projects on time and within budget"
      ]
    },
    {
      "title": "AI Research Intern",
      "company": "Data Insights Lab",
      "location": None,
      "start_date": "2022",
      "end_date": "2023",
      "responsibilities": [
        "Conducted research on machine learning algorithms, contributing to a publication in the Journal of AI Research",
        "Developed predictive models that increased data processing efficiency by 15%"
      ]
    },
    {
      "title": "Junior Developer",
      "company": "CodeCrafters LLC",
      "location": None,
      "start_date": "2021",
      "end_date": "2022",
      "responsibilities": [
        "Assisted in developing e-commerce platforms using Go and Kubernetes",
        "Implemented features that enhanced user experience and boosted sales by 10%"
      ]
    }
  ],
  "volunteer_experience": [],
  "projects": [
    {
      "name": "AI-Powered Chatbot",
      "description": "Designed and implemented a chatbot using TensorFlow and Python, capable of handling customer inquiries with a 90% accuracy rate. Deployed the solution using Docker and Kubernetes for scalability.",
      "role": None,
      "technologies": [
        "TensorFlow",
        "Python",
        "Docker",
        "Kubernetes"
      ],
      "link": "GitHub"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect",
      "issuing_organization": None,
      "issue_date": "2023",
      "expiration_date": None,
      "credential_id": None,
      "credential_url": None
    }
  ],
  "awards": [],
  "languages": [
    {
      "language": "English",
      "proficiency": "Native proficiency"
    },
    {
      "language": "Spanish",
      "proficiency": "Professional working proficiency"
    }
  ],
  "publications": [],
  "interests": [],
  "cover_letter_stories": [
    {
      "title": "My Motivation",
      "content": "I am driven by a passion for technology and its potential to create meaningful change. I thrive in dynamic environments where I can apply my skills to develop innovative solutions. My goal is to continuously grow as a professional and contribute to projects that make a positive impact on society."
    }
  ]
}

@pytest.fixture
def application_data_json():
    return {
        "position_information": {
            "job_title": "Internship",
            "department": "Property & Casualty, Employee Benefits, Real Estate, Entertainment, Private Client and Commercial Lines Teams",
            "location": "New York, NY",
            "employment_type": "Internship",
            "description": "An exciting, 10-week, paid, on-site Internship experience awaits! Gain real life experience into the world of Insurance Brokerage. You will work within a high-energy, fast paced environment that is both competitive and fun. This role will afford the opportunity to work on-site in our New York, NY office for Summer 2025.",
            "responsibilities": [
                "Receive targeted business and technical training with a greater understanding of the Retail Brokerage Insurance industry",
                "Become acclimated to working in an environment dedicated to exceeding client expectations and delivering products and modules distinct to unique client needs",
                "Work with account and project teams to deliver business-focused initiatives and strategic recommendations",
                "Be presented with real world business, risk management, and insurance experience and learn to apply the concepts you've learned in the classroom through project work",
                "Shadow team members on meetings with clients and attend client decision meetings and conference calls",
                "Be assigned a dedicated Internship Mentor & Internship Ambassador during your Internship experience",
                "Engage weekly with Sr. Leaders across the company on our renowned 'Leadership Perspective' Series",
                "Participate weekly in our 'Professional Insights' Series (Creating/Updating Your LinkedIn profile, Interviewing Best Practices, Resume Writing, Job Search tips etc.)",
                "Be actively involved in our 'RiskMate' Peer Program for breakout sessions throughout the summer"
            ],
            "requirements": [
                "Must be a Rising Senior (Anticipated Graduation 5/26)",
                "Must be available for entire 10-week program, including an Intern Summit to be held in Boston, MA June 2nd – June 4th (expenses paid)",
                "3.0 GPA or higher (Transcript required prior to interview)",
                "Preference for Finance, Risk Management or Economics majors (previous insurance internship experience may be considered in lieu of)",
                "Must be available to interview in December/January",
                "Exceptional organizational and time-management skills",
                "Must be detailed oriented and proficient with MS Office Suite"
            ],
            "posted_date": None,
            "closing_date": None
        },
        "company_profile": {
            "name": "Risk Strategies",
            "website": None,
            "description": "Risk Strategies is the 9th largest privately held US brokerage firm offering comprehensive risk management advice, insurance and reinsurance placement for Property & Casualty, Employee Benefits, Private Client Services, as well as consulting modules and financial & wealth solutions.",
            "industry": "Insurance",
            "size": "5,400 employees"
        },
        "custom_sections": [],
        "extra_text": [
            "Industry recognition includes being certified a 2024 Rise Elite Internship Program Recipient, Great Place to Work in 2025 and is on the Inc. 5000 list as one of America's fastest growing private companies.",
            "At Risk Strategies Company, base pay is one part of our total compensation package, which also includes a comprehensive suite of benefits, including medical, dental, vision, disability, and life insurance, retirement savings, and paid time off and paid holidays for eligible employees. The total compensation for a position may also include other elements dependent on the position offered. The expected base pay range for this position is $21/hour."
        ]
    }


import pytest


@pytest.fixture
def applicant_resume_txt():
    return """
    Alex Johnson is a Software Engineer with a B.S. in Computer Science from Tech University, class of 2023. He is currently enrolled in an M.S. program in Artificial Intelligence at Innovation University, expected to graduate in 2025.

His technical skills include programming languages (JavaScript with React, Python with Django, and Go), AI & machine learning (TensorFlow, PyTorch), DevOps & cloud technologies (Docker, Kubernetes, AWS, GCP), infrastructure (Linux, Nginx, Terraform, Git), testing (Jest, Mocha, Test-Driven Development), and blockchain (Smart Contracts, Ethereum, Hyperledger). He also has strong skills in team leadership, project management, agile methodologies, and technical mentoring.

Professional Experience

    Software Developer at Web Solutions Inc. (2023 – Present): Developed and maintained web applications using React and Django, improving client satisfaction by 25%. Collaborated with cross-functional teams to deliver projects on time and within budget.

    AI Research Intern at Data Insights Lab (2022 – 2023): Conducted research on machine learning algorithms, contributing to a publication in the Journal of AI Research. Developed predictive models that increased data processing efficiency by 15%.

    Junior Developer at CodeCrafters LLC (2021 – 2022): Assisted in developing e-commerce platforms using Go and Kubernetes. Implemented features that enhanced user experience and boosted sales by 10%.

Technical Projects

    AI-Powered Chatbot (2024, GitHub): Designed and implemented a chatbot using TensorFlow and Python, capable of handling customer inquiries with a 90% accuracy rate. Deployed the solution using Docker and Kubernetes for scalability.

Certifications

    AWS Certified Solutions Architect – 2023

Languages

    English: Native proficiency
    Spanish: Professional working proficiency

Contact Information

    Phone: +1 555 123-4567
    Email: alex.johnson@example.com
    LinkedIn: linkedin.com/in/alex-johnson-123456
    GitHub: github.com/alexjohnson
    """


@pytest.fixture
def linkedin_profile_txt():
    return """
    Alex Johnson is a dedicated Software Engineer specializing in full-stack development and artificial intelligence. With over 2 years of experience, he has a proven track record of building robust web applications and AI models. Alex is passionate about leveraging technology to solve real-world problems and is always eager to learn and adopt new technologies.

    In his current role at Web Solutions Inc., Alex has led the development of several key projects, resulting in a significant increase in client satisfaction. He is also pursuing an M.S. in Artificial Intelligence to deepen his expertise in the field.

    Outside of work, Alex contributes to open-source projects and enjoys mentoring junior developers. He is an advocate for continuous learning and believes in the power of collaboration to drive innovation.

    Skills: JavaScript, React, Python, Django, Go, TensorFlow, Docker, Kubernetes, AWS, Agile Methodologies, Team Leadership
    """


@pytest.fixture
def applicant_custom_txt():
    return """
    My Motivation
    I am driven by a passion for technology and its potential to create meaningful change. I thrive in dynamic environments where I can apply my skills to develop innovative solutions. My goal is to continuously grow as a professional and contribute to projects that make a positive impact on society.
    """



@pytest.fixture
def application_raw_text():
    return """
 About the job

An exciting, 10-week, paid, on-site Internship experience awaits! Gain real life experience into the world of Insurance Brokerage. You will work within a high-energy, fast paced environment that is both competitive and fun. This role will afford the opportunity to work on-site in our New York, NY office for Summer 2025. Internship opportunities are within our Property & Casualty or Employee Benefits practices and include opportunities on our Real Estate, Entertainment, Employee Benefits, Private Client and Commercial Lines Teams and others.


Our summer Internship program offers the chance to have practical, real-world experience at a Top 16 P&C Broker. As a part of the program, you will have the opportunity to work on business specific projects where you will gain knowledge and experience to supplement and strengthen your skills.


You will:

    Receive targeted business and technical training with a greater understanding of the Retail Brokerage Insurance industry
    Become acclimated to working in an environment dedicated to exceeding client expectations and delivering products and modules distinct to unique client needs
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

consulting modules and financial & wealth solutions. With over 200 offices and more than 5,400 employees, Risk Strategies is as part of the Accession Risk Management Group family of companies.


Industry recognition includes being certified a 2024 Rise Elite Internship Program Recipient, Great Place to Work in 2025 and is on the Inc. 5000 list as one of America’s fastest growing private companies.



At Risk Strategies Company, base pay is one part of our total compensation package, which also includes a comprehensive suite of benefits, including medical, dental, vision, disability, and life insurance, retirement savings, and paid time off and paid holidays for eligible employees. The total compensation for a position may also include other elements dependent on the position offered. The expected base pay range for this position is $21/hour.
    """