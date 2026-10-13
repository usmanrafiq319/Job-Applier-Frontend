import logging
import re

from app.core.job_skill_catalog import (
    HIGH_IMPORTANCE_WORDS,
    JOB_SKILL_ALIASES,
    OPTIONAL_REQUIREMENT_WORDS,
)

from app.integrations.llm.groq_llm import (
    GroqConfigurationError,
    GroqGenerationError,
)

from app.integrations.llm.llm_router import (
    LLMMode,
    LLMRouter,
)

from app.schemas.requirement_extraction import (
    RequirementExtractionOutput,
)


logger = logging.getLogger(__name__)


class RequirementExtractionService:

    def __init__(self):

        self.llm_router = LLMRouter()


    async def extract(
        self,
        job_title: str,
        description: str
    ) -> tuple[list[dict], str]:

        try:

            requirements = (
                await self._extract_with_groq(
                    job_title,
                    description
                )
            )

            if requirements:

                return (
                    requirements,
                    "groq"
                )

        except (
            GroqConfigurationError,
            GroqGenerationError
        ) as exc:

            logger.warning(
                "Groq requirement extraction "
                "failed. Using deterministic "
                "fallback. Error: %s",
                exc
            )


        requirements = (
            self._extract_deterministically(
                description
            )
        )

        return (
            requirements,
            "deterministic"
        )


    async def _extract_with_groq(
        self,
        job_title: str,
        description: str
    ) -> list[dict]:

        prompt = f"""
Job title:
{job_title}

Job description:
{description}

Extract the important requirements from this
job description.

Requirement types:

SKILL
- technical skill, framework, language,
  database, platform, tool, methodology

EXPERIENCE
- years of experience or work experience

EDUCATION
- degree, qualification, certification

RESPONSIBILITY
- important duties the candidate must perform

OTHER
- important requirement that does not fit
  another category

Rules:

1. Keep each requirement concise.

2. For SKILL requirements, set skill_name
   to the canonical skill name.

Examples:
"angular" -> "Angular"
"asp net core" -> "ASP.NET Core"
"postgres" -> "PostgreSQL"

3. For non-SKILL requirements,
   skill_name must be null.

4. Set is_required=false when wording includes
   concepts such as:
   preferred,
   nice to have,
   bonus,
   plus,
   advantage.

5. Importance should be:

HIGH:
must-have, required, minimum, strongly emphasized

MEDIUM:
normal requirement

LOW:
optional/preferred/nice-to-have

6. Do not invent requirements that are not
   present in the description.

7. Do not duplicate requirements.
""".strip()


        result = (
            await self.llm_router
            .generate_structured(
                prompt=prompt,

                schema=(
                    RequirementExtractionOutput
                ),

                system_prompt=(
                    "You extract structured "
                    "requirements from software "
                    "job descriptions. Return only "
                    "requirements supported by the "
                    "provided job description."
                ),

                mode=LLMMode.FAST
            )
        )


        return [
            item.model_dump()
            for item in result.requirements
        ]


    def _contains_alias(
        self,
        text: str,
        alias: str
    ) -> bool:

        pattern = (
            rf"(?<![A-Za-z0-9])"
            rf"{re.escape(alias)}"
            rf"(?![A-Za-z0-9])"
        )


        return (
            re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )
            is not None
        )


    def _extract_deterministically(
        self,
        description: str
    ) -> list[dict]:

        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            description
        )


        found: dict[str, dict] = {}


        for canonical, aliases in (
            JOB_SKILL_ALIASES.items()
        ):

            matching_sentence = None


            for sentence in sentences:

                candidates = [
                    canonical,
                    *aliases,
                ]


                if any(
                    self._contains_alias(
                        sentence,
                        candidate
                    )
                    for candidate
                    in candidates
                ):

                    matching_sentence = (
                        sentence
                    )

                    break


            if matching_sentence is None:
                continue


            lower_sentence = (
                matching_sentence
                .casefold()
            )


            optional = any(
                word in lower_sentence
                for word in
                OPTIONAL_REQUIREMENT_WORDS
            )


            high_importance = any(
                word in lower_sentence
                for word in
                HIGH_IMPORTANCE_WORDS
            )


            if optional:

                importance = "LOW"
                is_required = False

            elif high_importance:

                importance = "HIGH"
                is_required = True

            else:

                importance = "MEDIUM"
                is_required = True


            found[canonical] = {

                "text":
                    matching_sentence.strip(),

                "requirement_type":
                    "SKILL",

                "skill_name":
                    canonical,

                "is_required":
                    is_required,

                "importance":
                    importance,
            }


        return list(
            found.values()
        )