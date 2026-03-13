from sqlalchemy import Column, Integer, ForeignKey
from app.database.database import Base

class TeamStats(Base):
    __tablename__ = "team_stats"

    id = Column(Integer, primary_key=True, index=True)

    team_id = Column(Integer, ForeignKey("teams.id"))

    played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    losses = Column(Integer, default=0)

    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)

    points = Column(Integer, default=0)