from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    age = Column(Integer)
    email = Column(String(30), unique=True, index=True)
    working = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
