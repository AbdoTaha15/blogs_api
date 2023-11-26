from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./blogs.db"
engine = create_engine(DATABASE_URL, echo=True)


async def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine, future=True) as session:
        yield session
