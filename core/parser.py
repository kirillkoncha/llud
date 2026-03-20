from langchain_core.prompts import PromptTemplate

from core.languages import validate_glottolog
from core.schema import UDParse
from prompts.prompts import UD_PROMPT
from providers.llm import LLMProvider


class UDParser:
    def __init__(
        self, provider: LLMProvider, lang_code: str, prompt: PromptTemplate = UD_PROMPT
    ):
        if not validate_glottolog(lang_code):
            raise ValueError(f"Invalid Glottolog code: {lang_code}")
        self.provider = provider
        self.lang_code = lang_code
        self.prompt = prompt

    def parse(self, sentence: str) -> UDParse:
        prompt_text = self.prompt.format(sentence=sentence, lang_code=self.lang_code)
        try:
            tokenlist = self.provider.parse(prompt_text)
        except Exception as e:
            raise RuntimeError(f"Parsing failed: {e}")
        return UDParse(sentence=sentence, tokens=tokenlist)
