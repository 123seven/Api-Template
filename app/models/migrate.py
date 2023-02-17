from app.models.database import create_db_and_tables


def migrate() -> None:
    create_db_and_tables()

    print("Success migration!")


if __name__ == "__main__":
    migrate()
