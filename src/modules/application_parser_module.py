# File: src/modules/application_parser_module.py

from src.models.application_data import ApplicationData
from src.modules.application_parser.application_parser import ApplicationParser, PlainTextParser
from src.llm_wrappers.llm_providers import LLMProvider, OpenAILLMProvider
from src.persistance.application_repository import ApplicationRepository
from src.persistance.file_storage.file_application_repository import FileApplicationRepository
from src.persistance.utils import compute_hash


class ApplicationParserModule:
    def __init__(self,
                 llm_provider: LLMProvider = None,
                 parser: ApplicationParser = None,
                 repo: ApplicationRepository = None,
                 ):
        self.llm_provider = llm_provider or OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=3000)
        self.parser = parser or PlainTextParser(self.llm_provider)
        self.application_repo = repo or FileApplicationRepository()

    def parse(self, application_text: str) -> ApplicationData:
        key = compute_hash(application_text)
        stored_application = self.application_repo.get_application(key)
        if stored_application:
            print("Loading application data from repository.")
            return stored_application

        application_data = self.parser.parse(application_text)
        self.application_repo.store_application(key, application_data)
        return application_data