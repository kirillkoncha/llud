from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
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
        else:
            raise ValueError(f"Unsupported provider: {provider_type}")

        if self.provider_type == "openai":
            structured_output_method = "json_schema"
        else:
            structured_output_method = "function_calling"

        self.structured_llm = self.llm.with_structured_output(
            self.parse_model, method=structured_output_method
        )

    def parse(self, prompt_text: str) -> TokenList:
        return self.structured_llm.invoke(prompt_text)
