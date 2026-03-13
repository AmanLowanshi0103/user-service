from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.database import Base

class Fixture(Base):
    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)

    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))

    matchday = Column(Integer, index=True)   # week number

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)

    status = Column(String, default="scheduled")  # scheduled / played