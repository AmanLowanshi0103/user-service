from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.model.teamsmodels import Team

PREMIER_LEAGUE_TEAMS = [
    {"id": 1, "name": "Arsenal", "rating": 86},
    {"id": 2, "name": "Manchester City", "rating": 92},
    {"id": 3, "name": "Liverpool", "rating": 90},
    {"id": 4, "name": "Chelsea", "rating": 84},
    {"id": 5, "name": "Manchester United", "rating": 85},
    {"id": 6, "name": "Tottenham Hotspur", "rating": 83},
    {"id": 7, "name": "Newcastle United", "rating": 84},
    {"id": 8, "name": "Aston Villa", "rating": 83},
    {"id": 9, "name": "Brighton & Hove Albion", "rating": 82},
    {"id": 10, "name": "West Ham United", "rating": 80},
    {"id": 11, "name": "Crystal Palace", "rating": 78},
    {"id": 12, "name": "Fulham", "rating": 78},
    {"id": 13, "name": "Brentford", "rating": 79},
    {"id": 14, "name": "Wolverhampton Wanderers", "rating": 78},
    {"id": 15, "name": "Everton", "rating": 77},
    {"id": 16, "name": "Nottingham Forest", "rating": 76},
    {"id": 17, "name": "Bournemouth", "rating": 76},
    {"id": 18, "name": "Leicester City", "rating": 79},
    {"id": 19, "name": "Ipswich Town", "rating": 74},
    {"id": 20, "name": "Southampton", "rating": 75}
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

routerTeams=APIRouter(prefix="/teams")

@routerTeams.get("")
def getAllteams(db: Session=Depends(get_db)):
    dbTeams=db.query(Team).all()
    return dbTeams

@routerTeams.get("/{id}")
def getTeam(id,db: Session=Depends(get_db)):
    dbTeam=db.query(Team).filter(Team.id==id).first()
    return dbTeam

@routerTeams.post("/hydrate_teams")
def hydratealltheteams(db: Session=Depends(get_db)):
    for teams in PREMIER_LEAGUE_TEAMS:
        team = Team(**teams)
        db.add(team)
    db.commit()
    return {"messgae": "Teams sucssesiully added"}

     