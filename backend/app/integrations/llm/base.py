from abc import (
    ABC,
    abstractmethod,
)

from typing import TypeVar

from pydantic import BaseModel


T = TypeVar(
    "T",
    bound=BaseModel
)


class LLMProvider(ABC):

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:
        pass


    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: type[T],
        system_prompt: str | None = None
    ) -> T:
        pass