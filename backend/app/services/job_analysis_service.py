import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.job_skill_catalog import (
    JOB_SKILL_ALIASES,
)

from app.repositories.experience_repository import (
    ExperienceRepository,
)

from app.repositories.job_analysis_repository import (
    JobAnalysisRepository,
)

from app.repositories.job_repository import (
    JobRepository,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.repositories.project_repository import (
    ProjectRepository,
)

from app.repositories.skill_repository import (
    SkillRepository,
)

from app.schemas.job_analysis import (
    JobAnalysisResponse,
    JobAnalyzeRequest,
    JobRequirementResponse,
    RelevantEvidence,
)

from app.schemas.retrieval import (
    ResumeSearchRequest,
)

from app.services.requirement_extraction_service import (
    RequirementExtractionService,
)

from app.services.retrieval_service import (
    RetrievalService,
)


class AnalyzeProfileNotFoundError(Exception):
    pass


class AnalyzeJobNotFoundError(Exception):
    pass


class JobAnalysisService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.job_repository = (
            JobRepository()
        )

        self.skill_repository = (
            SkillRepository()
        )

        self.project_repository = (
            ProjectRepository()
        )

        self.experience_repository = (
            ExperienceRepository()
        )

        self.analysis_repository = (
            JobAnalysisRepository()
        )

        self.retrieval_service = (
            RetrievalService()
        )

        self.requirement_extraction_service = (
            RequirementExtractionService()
        )


    def _canonicalize_skill(
        self,
        value: str
    ) -> str:

        normalized = (
            value.strip().casefold()
        )

        for canonical, aliases in (
            JOB_SKILL_ALIASES.items()
        ):

            if (
                normalized
                == canonical.casefold()
            ):
                return canonical

            for alias in aliases:

                if (
                    normalized
                    == alias.casefold()
                ):
                    return canonical

        return value.strip()


    def _build_profile_skill_set(
        self,
        skill_rows,
        projects,
        experiences
    ) -> set[str]:

        skills: set[str] = set()

        # Skills explicitly added to profile
        for _, skill in skill_rows:

            skills.add(
                self._canonicalize_skill(
                    skill.name
                )
            )

        # Technologies used in projects
        for project in projects:

            for technology in (
                project.technologies
            ):

                skills.add(
                    self._canonicalize_skill(
                        technology
                    )
                )

        # Technologies used in experience
        for experience in experiences:

            for technology in (
                experience.technologies
            ):

                skills.add(
                    self._canonicalize_skill(
                        technology
                    )
                )

        return skills


    def _context_evidence(
        self,
        requirements: list[dict],
        projects,
        experiences
    ) -> list[RelevantEvidence]:

        # Only SKILL requirements belong in
        # project/experience technology matching.
        required_skills = {

            self._canonicalize_skill(
                item["skill_name"]
            )

            for item in requirements

            if (
                item.get(
                    "requirement_type"
                )
                == "SKILL"

                and item.get(
                    "skill_name"
                )
            )
        }

        if not required_skills:
            return []

        evidence: list[
            RelevantEvidence
        ] = []

        # -------------------------
        # Project evidence
        # -------------------------

        for project in projects:

            project_skills = {

                self._canonicalize_skill(
                    technology
                )

                for technology
                in project.technologies
            }

            overlap = (
                required_skills
                & project_skills
            )

            if not overlap:
                continue

            relevance = (
                len(overlap)
                / len(required_skills)
            )

            evidence.append(
                RelevantEvidence(
                    source="project",
                    source_id=str(
                        project.id
                    ),
                    title=project.title,
                    content=(
                        project.description
                    ),
                    relevance=round(
                        relevance,
                        4
                    )
                )
            )

        # -------------------------
        # Experience evidence
        # -------------------------

        for experience in experiences:

            experience_skills = {

                self._canonicalize_skill(
                    technology
                )

                for technology
                in experience.technologies
            }

            overlap = (
                required_skills
                & experience_skills
            )

            if not overlap:
                continue

            relevance = (
                len(overlap)
                / len(required_skills)
            )

            evidence.append(
                RelevantEvidence(
                    source="experience",
                    source_id=str(
                        experience.id
                    ),
                    title=(
                        f"{experience.role} "
                        f"at "
                        f"{experience.company}"
                    ),
                    content=(
                        experience.description
                    ),
                    relevance=round(
                        relevance,
                        4
                    )
                )
            )

        evidence.sort(
            key=lambda item:
                item.relevance,
            reverse=True
        )

        return evidence[:5]


    def _skill_score(
        self,
        requirements: list[dict],
        user_skills: set[str]
    ) -> tuple[
        float,
        list[str],
        list[str]
    ]:

        # Groq now returns several requirement
        # types. Only SKILL requirements should
        # participate in skill matching.
        skill_requirements = [

            requirement

            for requirement
            in requirements

            if (
                requirement.get(
                    "requirement_type"
                )
                == "SKILL"

                and requirement.get(
                    "skill_name"
                )
            )
        ]

        if not skill_requirements:

            return (
                0.0,
                [],
                []
            )

        total_weight = 0.0
        matched_weight = 0.0

        matched: list[str] = []
        missing: list[str] = []

        for requirement in (
            skill_requirements
        ):

            skill = (
                self._canonicalize_skill(
                    requirement["skill_name"]
                )
            )

            # Required + high importance
            # matters more.
            if (
                requirement.get(
                    "importance"
                )
                == "HIGH"
            ):
                weight = 1.5

            elif not requirement.get(
                "is_required",
                True
            ):
                weight = 0.5

            else:
                weight = 1.0

            total_weight += weight

            if skill in user_skills:

                matched.append(
                    skill
                )

                matched_weight += weight

            else:

                missing.append(
                    skill
                )

        if total_weight == 0:

            return (
                0.0,
                [],
                []
            )

        score = (
            matched_weight
            / total_weight
        ) * 100

        # Remove duplicates while preserving order.
        matched = list(
            dict.fromkeys(
                matched
            )
        )

        missing = list(
            dict.fromkeys(
                missing
            )
        )

        return (
            score,
            matched,
            missing
        )


    async def analyze_job(
        self,
        db: AsyncSession,
        payload: JobAnalyzeRequest
    ) -> JobAnalysisResponse:

        # ---------------------------------
        # 1. Load current profile
        # ---------------------------------

        profile = (
            await self.profile_repository
            .get_profile(db)
        )

        if profile is None:

            raise (
                AnalyzeProfileNotFoundError()
            )

        # ---------------------------------
        # 2. Load requested job
        # ---------------------------------

        job = (
            await self.job_repository
            .get_by_id(
                db,
                profile.id,
                payload.job_id
            )
        )

        if job is None:

            raise AnalyzeJobNotFoundError()

        # ---------------------------------
        # 3. Extract requirements
        #
        # Groq first.
        # Deterministic extractor if Groq fails.
        # ---------------------------------

        (
            requirements,
            extraction_source
        ) = (
            await self
            .requirement_extraction_service
            .extract(
                job_title=job.title,
                description=job.description
            )
        )

        # ---------------------------------
        # 4. Load profile context
        # ---------------------------------

        skill_rows = (
            await self.skill_repository
            .list_for_profile(
                db,
                profile.id
            )
        )

        projects = (
            await self.project_repository
            .list_for_profile(
                db,
                profile.id
            )
        )

        experiences = (
            await self.experience_repository
            .list_for_profile(
                db,
                profile.id
            )
        )

        # ---------------------------------
        # 5. Combine known candidate skills
        # ---------------------------------

        user_skills = (
            self._build_profile_skill_set(
                skill_rows,
                projects,
                experiences
            )
        )

        # ---------------------------------
        # 6. Calculate deterministic skill score
        # ---------------------------------

        (
            skill_score,
            matched_skills,
            missing_skills
        ) = self._skill_score(
            requirements,
            user_skills
        )

        # Count only actual skill requirements.
        skill_requirement_count = sum(

            1

            for requirement
            in requirements

            if (
                requirement.get(
                    "requirement_type"
                )
                == "SKILL"

                and requirement.get(
                    "skill_name"
                )
            )
        )

        # ---------------------------------
        # 7. Build semantic-search query
        # ---------------------------------

        search_terms = [

            self._canonicalize_skill(
                requirement[
                    "skill_name"
                ]
            )

            for requirement
            in requirements

            if (
                requirement.get(
                    "requirement_type"
                )
                == "SKILL"

                and requirement.get(
                    "skill_name"
                )
            )
        ]

        resume_query = (
            f"{job.title}. "
            f"{' '.join(search_terms)}. "
            f"{job.description}"
        )

        # ---------------------------------
        # 8. RAG: retrieve relevant
        #    resume chunks with pgvector
        # ---------------------------------

        resume_results = (
            await self.retrieval_service
            .search_resume(
                db,

                ResumeSearchRequest(
                    query=resume_query,
                    limit=payload.resume_limit
                )
            )
        )

        resume_evidence = [

            RelevantEvidence(
                source="resume",

                source_id=str(
                    result.chunk_id
                ),

                title=(
                    f"Resume page "
                    f"{result.page_number}"
                ),

                content=result.content,

                relevance=(
                    result.similarity
                )
            )

            for result
            in resume_results
        ]

        # ---------------------------------
        # 9. Find relevant Projects /
        #    Experience using technologies
        # ---------------------------------

        context_evidence = (
            self._context_evidence(
                requirements,
                projects,
                experiences
            )
        )

        all_evidence = (
            resume_evidence
            + context_evidence
        )

        # ---------------------------------
        # 10. Resume RAG score
        # ---------------------------------

        resume_score = 0.0

        if resume_evidence:

            resume_score = (
                max(
                    evidence.relevance

                    for evidence
                    in resume_evidence
                )
                * 100
            )

        # ---------------------------------
        # 11. Project / Experience score
        # ---------------------------------

        context_score = 0.0

        if context_evidence:

            context_score = (
                max(
                    evidence.relevance

                    for evidence
                    in context_evidence
                )
                * 100
            )

        # ---------------------------------
        # 12. Build weighted score
        # ---------------------------------

        components: list[
            tuple[float, float]
        ] = []

        # Important correction:
        # only add skill scoring if actual
        # SKILL requirements were extracted.
        if skill_requirement_count > 0:

            components.append(
                (
                    skill_score,
                    0.70
                )
            )

        if resume_evidence:

            components.append(
                (
                    resume_score,
                    0.20
                )
            )

        if context_evidence:

            components.append(
                (
                    context_score,
                    0.10
                )
            )

        if components:

            weight_sum = sum(
                weight

                for _, weight
                in components
            )

            match_score = round(

                sum(
                    score * weight

                    for score, weight
                    in components
                )

                / weight_sum
            )

        else:

            match_score = 0

        match_score = max(
            0,
            min(
                100,
                match_score
            )
        )

        # ---------------------------------
        # 13. Recommendation
        # ---------------------------------

        if match_score >= 80:

            recommendation = (
                "STRONG_MATCH"
            )

            job.status = (
                "HIGH_MATCH"
            )

        elif match_score >= 60:

            recommendation = (
                "POSSIBLE_MATCH"
            )

            job.status = (
                "ANALYZED"
            )

        else:

            recommendation = (
                "LOW_MATCH"
            )

            job.status = (
                "LOW_MATCH"
            )

        # ---------------------------------
        # 14. Build summary
        # ---------------------------------

        summary = (
            f"Matched "
            f"{len(matched_skills)} "
            f"of "
            f"{skill_requirement_count} "
            f"detected skill requirements. "
            f"Overall match score: "
            f"{match_score}%. "
            f"Requirements extracted using "
            f"{extraction_source}."
        )

        # ---------------------------------
        # 15. Replace old job requirements
        # ---------------------------------

        requirement_rows = (
            await self.analysis_repository
            .replace_requirements(
                db,
                job.id,
                requirements
            )
        )

        # ---------------------------------
        # 16. Create/update analysis
        # ---------------------------------

        analysis = (
            await self.analysis_repository
            .upsert_analysis(
                db,
                job.id,
                {
                    "match_score":
                        match_score,

                    "recommendation":
                        recommendation,

                    "matched_skills":
                        matched_skills,

                    "missing_skills":
                        missing_skills,

                    "relevant_experience": [
                        item.model_dump()

                        for item
                        in all_evidence
                    ],

                    "summary":
                        summary,
                }
            )
        )

        # ---------------------------------
        # 17. Commit everything together
        # ---------------------------------

        await db.commit()

        await db.refresh(
            analysis
        )

        # ---------------------------------
        # 18. Build API response
        # ---------------------------------

        return JobAnalysisResponse(

            id=analysis.id,

            job_id=job.id,

            match_score=(
                analysis.match_score
            ),

            recommendation=(
                analysis.recommendation
            ),

            matched_skills=(
                analysis.matched_skills
            ),

            missing_skills=(
                analysis.missing_skills
            ),

            relevant_experience=[

                RelevantEvidence(
                    **item
                )

                for item
                in analysis.relevant_experience
            ],

            summary=analysis.summary,

            analyzed_at=(
                analysis.analyzed_at
            ),

            requirements=[

                JobRequirementResponse(
                    id=row.id,

                    text=row.text,

                    requirement_type=(
                        row.requirement_type
                    ),

                    skill_name=(
                        row.skill_name
                    ),

                    is_required=(
                        row.is_required
                    ),

                    importance=(
                        row.importance
                    )
                )

                for row
                in requirement_rows
            ]
        )