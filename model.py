from sqlalchemy import Column, Integer, String
from database import Base


class ProjectTable(Base):
    __tablename__ = 'proj'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250))
    description = Column(String(250))
    video = Column(String(250))
    image = Column(String(250))
