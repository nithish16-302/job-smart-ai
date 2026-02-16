from app.db.session import Base, engine
from app.models import user, resume_profile

def init_db():
    Base.metadata.create_all(bind=engine)
