from alembic import command
from alembic.config import Config

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def init_postgresql():
    alembic_config = Config(
        str(PROJECT_ROOT / "alembic.ini"),
    )

    command.upgrade(
        alembic_config,
        "head"
    )

    print("PostgreSQL schema initialized")

if __name__ == "__main__":
    init_postgresql()