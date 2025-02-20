import os
import pytest
from src.llm_wrappers.llm_providers import OpenAILLMProvider

@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"],
    reason="Skipping integration test because OPENAI_API_KEY is not set"
)
def test_openai_llm_connection():
    """
    Integration test to verify that OpenAILLMProvider successfully connects to OpenAI API
    and returns a valid response.
    """
    llm = OpenAILLMProvider(model="gpt-4o", temperature=0.3, max_tokens=50)

    test_prompt = "Generate a short greeting message."

    response = llm.complete(test_prompt)

    assert response is not None, "Response should not be None"
    assert isinstance(response, str), "Response should be a string"
    assert len(response.strip()) > 0, "Response should not be empty"
    print(f"OpenAI LLM Response: {response}")