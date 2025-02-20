import os
from abc import ABC, abstractmethod
import openai


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        """
        Given a prompt, return the completion result from the LLM.
        """
        pass

class OpenAILLMProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4", temperature: float = 0.3, max_tokens: int = 1500):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a resume builder that produces valid LaTeX output."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content.strip()