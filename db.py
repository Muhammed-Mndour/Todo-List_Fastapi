from sqlmodel import Session, SQLModel, create_engine

engine = create_engine("sqlite:///db.sqlite", echo=True)




def get_session():
    with Session(engine) as session:
        yield session

