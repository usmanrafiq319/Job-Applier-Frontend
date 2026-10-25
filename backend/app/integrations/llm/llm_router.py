from enum import Enum

from app.integrations.llm.base import T

from app.integrations.llm.gemini_llm import (
    GeminiLLM,
)

from app.integrations.llm.groq_llm import (
    GroqLLM,
)


class LLMMode(str,Enum):

    FAST = "fast"

    ADVANCED = "advanced"


class LLMRouter:

    def __init__(self):

        self.groq = GroqLLM()

        self.gemini = GeminiLLM()


    def _provider(
        self,
        mode: LLMMode
    ):

        if mode == LLMMode.ADVANCED:

            return self.gemini


        return self.groq


    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        mode: LLMMode = LLMMode.FAST
    ) -> str:

        provider = self._provider(
            mode
        )


        return await provider.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
        )


    async def generate_structured(
        self,
        prompt: str,
        schema: type[T],
        system_prompt: str | None = None,
        mode: LLMMode = LLMMode.FAST
    ) -> T:

        provider = self._provider(
            mode
        )


        return await provider.generate_structured(
            prompt=prompt,
            schema=schema,
            system_prompt=system_prompt,
        )