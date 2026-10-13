import json

from groq import AsyncGroq

from pydantic import BaseModel

from app.core.config import settings

from app.integrations.llm.base import (
    LLMProvider,
    T,
)


class GroqConfigurationError(Exception):
    pass


class GroqGenerationError(Exception):
    pass


class GroqLLM(
    LLMProvider
):

    def __init__(self):

        self.client = None


    def _get_client(self) -> AsyncGroq:

        if not settings.groq_api_key:

            raise GroqConfigurationError(
                "GROQ_API_KEY is not configured"
            )

        if self.client is None:

            self.client = AsyncGroq(
                api_key=settings.groq_api_key
            )

        return self.client


    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:

        client = self._get_client()


        messages = []


        if system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )


        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )


        try:

            response = (
                await client.chat
                .completions.create(
                    model=settings.groq_model,
                    messages=messages,
                    temperature=0.2,
                )
            )


            content = (
                response
                .choices[0]
                .message
                .content
            )


            if not content:

                raise GroqGenerationError(
                    "Groq returned an empty response"
                )


            return content.strip()


        except GroqGenerationError:
            raise

        except Exception as exc:

            raise GroqGenerationError(
                "Groq generation failed"
            ) from exc


    async def generate_structured(
        self,
        prompt: str,
        schema: type[T],
        system_prompt: str | None = None
    ) -> T:

        client = self._get_client()


        messages = []


        if system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )


        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )


        try:

            response = (
                await client.chat
                .completions.create(
                    model=settings.groq_model,
                    messages=messages,
                    temperature=0,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name":
                                schema.__name__,

                            "strict":
                                False,

                            "schema":
                                schema.model_json_schema(),
                        },
                    },
                )
            )


            content = (
                response
                .choices[0]
                .message
                .content
            )


            if not content:

                raise GroqGenerationError(
                    "Groq returned an empty "
                    "structured response"
                )


            data = json.loads(
                content
            )


            return schema.model_validate(
                data
            )


        except GroqGenerationError:
            raise

        except Exception as exc:

            raise GroqGenerationError(
                "Groq structured generation failed"
            ) from exc