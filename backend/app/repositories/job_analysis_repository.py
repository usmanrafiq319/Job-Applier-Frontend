import uuid

from sqlalchemy import (
    delete,
    select,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.job_analysis import (
    JobAnalysis,
)

from app.models.job_requirement import (
    JobRequirement,
)


class JobAnalysisRepository:

    async def replace_requirements(
        self,
        db: AsyncSession,
        job_id: uuid.UUID,
        requirements: list[dict]
    ) -> list[JobRequirement]:

        await db.execute(
            delete(JobRequirement)
            .where(
                JobRequirement.job_id
                == job_id
            )
        )


        created = []


        for data in requirements:

            requirement = JobRequirement(
                job_id=job_id,
                **data
            )

            db.add(requirement)

            created.append(
                requirement
            )


        await db.flush()

        return created


    async def get_analysis(
        self,
        db: AsyncSession,
        job_id: uuid.UUID
    ) -> JobAnalysis | None:

        result = await db.execute(
            select(JobAnalysis)
            .where(
                JobAnalysis.job_id
                == job_id
            )
        )

        return result.scalar_one_or_none()


    async def upsert_analysis(
        self,
        db: AsyncSession,
        job_id: uuid.UUID,
        data: dict
    ) -> JobAnalysis:

        analysis = await self.get_analysis(
            db,
            job_id
        )


        if analysis is None:

            analysis = JobAnalysis(
                job_id=job_id,
                **data
            )

            db.add(
                analysis
            )

        else:

            for key, value in data.items():

                setattr(
                    analysis,
                    key,
                    value
                )


        await db.flush()

        return analysis