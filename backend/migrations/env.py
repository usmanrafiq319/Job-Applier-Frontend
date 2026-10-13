import asyncio
import selectors
from pgvector.sqlalchemy import VECTOR
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.base import Base

import app.models

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

def render_item(
    type_,
    obj,
    autogen_context
):

    if (
        type_ == "type"
        and isinstance(
            obj,
            VECTOR
        )
    ):

        autogen_context.imports.add(
            "from pgvector.sqlalchemy import VECTOR"
        )

        return (
            f"VECTOR({obj.dim})"
        )


    return False


def run_migrations_offline() -> None:

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
        render_item=render_item
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_item=render_item
        
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:

    connectable = create_async_engine(
        settings.database_url,
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:

        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


def run_migrations_online() -> None:

    loop_factory = lambda: asyncio.SelectorEventLoop(
        selectors.SelectSelector()
    )

    asyncio.run(
        run_async_migrations(),
        loop_factory=loop_factory
    )


if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()