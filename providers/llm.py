from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_gigachat import GigaChat
from pydantic import BaseModel

from core.schema import TokenList


class LLMProvider:
    """LLM provider using structured output (with_structured_output)."""

    def __init__(
        self,
        provider_type: str,
        model_name: str,
        api_key: str = None,
        temperature: float = 0,
        parse_model: BaseModel = TokenList,
        ca_bundle_path: str = None,
    ):
        self.provider_type = provider_type.lower()
        self.temperature = temperature
        self.parse_model = parse_model

        if self.provider_type == "openai":
            self.llm = ChatOpenAI(
                model_name=model_name, temperature=temperature, openai_api_key=api_key
            )
        elif self.provider_type == "mistral":
            self.llm = ChatMistralAI(
                model_name=model_name, temperature=temperature, api_key=api_key
            )
        elif self.provider_type == "gigachat":
            self.llm = GigaChat(
                model=model_name,
                temperature=temperature,
                credentials=api_key,
                ca_bundle_file=ca_bundle_path,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider_type}")

        if self.provider_type == "openai":
            self.structured_llm = self.llm.with_structured_output(
                self.parse_model, method="json_schema"
            )
        else:
            self.structured_llm = self.llm.with_structured_output(
                self.parse_model, method="json_mode"
            )

    def parse(self, prompt_text: str) -> TokenList:
        return self.structured_llm.invoke(prompt_text)
