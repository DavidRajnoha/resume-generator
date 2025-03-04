import os
from abc import ABC, abstractmethod
import anthropic


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        """
        Given a prompt, return the completion result from the LLM.
        """
        pass


class AnthropicLLMProvider(LLMProvider):
    def __init__(self, model: str = "claude-3-7-sonnet-20250219", temperature: float = 0.3, max_tokens: int = 1500):
        """
        Initialize the Anthropic Claude LLM provider.

        Args:
            model: The Claude model to use (e.g., "claude-3-opus-20240229", "claude-3-sonnet-20240229")
            temperature: Controls randomness. Lower is more deterministic (0-1)
            max_tokens: Maximum number of tokens to generate
        """
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        """
        Given a prompt, return the completion result from Claude.

        Args:
            prompt: The prompt to send to Claude

        Returns:
            The response from Claude, with any markdown code blocks removed
        """
        system_prompt = "You are a resume and cover letter builder that produces valid LaTeX output."

        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_str = response.content[0].text

        # Strip the ```LANGUAGE\n and ``` from the beginning and end of a response
        if response_str.startswith("```"):
            # Find the first newline after the language specifier
            first_newline = response_str.find("\n")
            if first_newline != -1:
                response_str = response_str[first_newline + 1:]

        if response_str.endswith("```"):
            # Find the last newline before the closing backticks
            last_newline = response_str.rfind("\n", 0, response_str.rfind("```"))
            if last_newline != -1:
                response_str = response_str[:last_newline]
            else:
                # If no newline found, just remove the backticks
                response_str = response_str[:-3].strip()

        return response_str.strip()