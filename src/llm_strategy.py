import os
import sys
from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

try:
    from src.config import MISTRAL_API_KEY, LLM_PROVIDER
except ImportError:
    # Handle direct script executions
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import MISTRAL_API_KEY, LLM_PROVIDER

class LLMProviderStrategy(ABC):
    """Abstract Strategy class defining the interface for obtaining the LLM."""
    
    @abstractmethod
    def get_llm(self, temperature: float = 0.0) -> BaseChatModel:
        """Returns a LangChain BaseChatModel instance."""
        pass

class MistralProviderStrategy(LLMProviderStrategy):
    """Mistral AI LLM Provider Strategy implementation."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def get_llm(self, temperature: float = 0.0) -> BaseChatModel:
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(
            mistral_api_key=self.api_key,
            model="mistral-large-latest",
            temperature=temperature
        )

class MockProviderStrategy(LLMProviderStrategy):
    """Mock LLM Provider Strategy implementation for local testing/evals."""
    
    def get_llm(self, temperature: float = 0.0) -> BaseChatModel:
        from langchain_community.chat_models import FakeListChatModel
        return FakeListChatModel(responses=["Mock LLM Response"])

def get_llm_provider(provider_name: str = None, api_key: str = None) -> BaseChatModel:
    """
    Factory helper that returns a BaseChatModel instance using the strategy
    determined by LLM_PROVIDER configuration.
    """
    if provider_name is None:
        provider_name = LLM_PROVIDER
    if api_key is None:
        api_key = MISTRAL_API_KEY
        
    if provider_name.lower() == "mistral":
        if not api_key:
            raise ValueError("MISTRAL_API_KEY must be set in config to use Mistral provider.")
        strategy = MistralProviderStrategy(api_key)
    elif provider_name.lower() == "mock":
        strategy = MockProviderStrategy()
    else:
        raise ValueError(f"Unsupported LLM provider Strategy: {provider_name}")
        
    return strategy.get_llm()
