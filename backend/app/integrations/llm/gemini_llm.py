import asyncio

from google import genai
from google.genai import types

from app.core.config import settings

from app.integrations.llm.base import (
    LLMProvider,
    T,
)


class GeminiLLMConfigurationError(
    Exception
):
    pass


class GeminiLLMGenerationError(
    Exception
):
    pass


class GeminiLLM(
    LLMProvider
):

    def __init__(self):

        self.client = None


    def _get_client(self):

        if not settings.gemini_api_key:

            raise GeminiLLMConfigurationError(
                "GEMINI_API_KEY is not configured"
            )


        if self.client is None:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )


        return self.client


    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:

        client = self._get_client()


        try:

            config = (
                types.GenerateContentConfig(
                    temperature=0.2,
                    system_instruction=(
                        system_prompt
                    ),
                )
            )


            response = await asyncio.to_thread(
                client.models.generate_content,
                model=settings.gemini_llm_model,
                contents=prompt,
                config=config,
            )


            if not response.text:

                raise GeminiLLMGenerationError(
                    "Gemini returned an empty response"
                )


            return response.text.strip()


        except GeminiLLMGenerationError:
            raise

        except Exception as exc:

            raise GeminiLLMGenerationError(
                "Gemini generation failed"
            ) from exc


    async def generate_structured(
        self,
        prompt: str,
        schema: type[T],
        system_prompt: str | None = None
    ) -> T:

        client = self._get_client()


        try:

            config = (
                types.GenerateContentConfig(
                    temperature=0,
                    system_instruction=(
                        system_prompt
                    ),
                    response_mime_type=(
                        "application/json"
                    ),
                    response_schema=schema,
                )
            )


            response = await asyncio.to_thread(
                client.models.generate_content,
                model=settings.gemini_llm_model,
                contents=prompt,
                config=config,
            )


            if not response.text:

                raise GeminiLLMGenerationError(
                    "Gemini returned an empty "
                    "structured response"
                )


            return schema.model_validate_json(
                response.text
            )


        except GeminiLLMGenerationError:
            raise

        except Exception as exc:

            raise GeminiLLMGenerationError(
                "Gemini structured generation failed"
            ) from exc