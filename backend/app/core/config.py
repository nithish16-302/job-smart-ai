import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobsmart.db")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALG = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24
