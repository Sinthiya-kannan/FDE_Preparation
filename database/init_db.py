from database.base import Base
from database.connection import engine

from models.customer import Customer
from models.user import User
from models.invitation import Invitation


def init_db():
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL tables created successfully")


if __name__ == "__main__":
    init_db()