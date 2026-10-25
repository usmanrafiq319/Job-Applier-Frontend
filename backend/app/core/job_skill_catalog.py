# This is the deterministic dictionary of known technical skills and their aliases.	It lets your fallback logic understand that values such as postgres, PostgreSQL, or asp net core refer to canonical skills and also defines words for required/optional importance.

JOB_SKILL_ALIASES: dict[str, list[str]] = {

    "Python": [
        "python",
    ],

    "FastAPI": [
        "fastapi",
        "fast api",
    ],

    "C#": [
        "c#",
        "c sharp",
    ],

    ".NET": [
        ".net",
        "dotnet",
    ],

    "ASP.NET Core": [
        "asp.net core",
        "asp net core",
    ],

    "Entity Framework Core": [
        "entity framework core",
        "ef core",
    ],

    "Angular": [
        "angular",
    ],

    "TypeScript": [
        "typescript",
        "type script",
    ],

    "JavaScript": [
        "javascript",
        "java script",
    ],

    "HTML": [
        "html",
    ],

    "CSS": [
        "css",
    ],

    "Tailwind CSS": [
        "tailwind",
        "tailwind css",
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres",
    ],

    "SQL Server": [
        "sql server",
        "mssql",
    ],

    "MySQL": [
        "mysql",
    ],

    "SQLite": [
        "sqlite",
    ],

    "SQL": [
        "sql",
    ],

    "REST API": [
        "rest api",
        "restful api",
        "restful services",
        "rest services",
    ],

    "Git": [
        "git",
    ],

    "GitHub": [
        "github",
    ],

    "Docker": [
        "docker",
    ],

    "Azure": [
        "azure",
    ],

    "AWS": [
        "aws",
        "amazon web services",
    ],

    "SignalR": [
        "signalr",
        "signal r",
    ],

    "Django": [
        "django",
    ],

    "LangChain": [
        "langchain",
        "lang chain",
    ],

    "LangGraph": [
        "langgraph",
        "lang graph",
    ],

    "RAG": [
        "rag",
        "retrieval augmented generation",
    ],

    "pgvector": [
        "pgvector",
    ],

    "Supabase": [
        "supabase",
    ],

    "Redis": [
        "redis",
    ],
}


OPTIONAL_REQUIREMENT_WORDS = (
    "plus",
    "preferred",
    "nice to have",
    "bonus",
    "advantage",
)


HIGH_IMPORTANCE_WORDS = (
    "required",
    "must",
    "strong experience",
    "proficient",
    "minimum",
)