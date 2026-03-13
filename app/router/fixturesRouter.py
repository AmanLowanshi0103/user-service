from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.model.teamsmodels import Team
from app.model.fixtures import Fixture
from app.service.genrator import generate_round_robin
from app.service.simulation import simulate_match
from app.service.statsupdate import update_team_stats
from app.model.teamsstats import TeamStats


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

routerFix=APIRouter(prefix="/fixtures")

@routerFix.get("/health")
def root_health():
    return {"success":"everthing is working fine"}


@routerFix.post("/generate-fix")
def generate_fixtures(db: Session = Depends(get_db)):

    existing = db.query(Fixture).first()
    if existing:
        return {"message": "Fixtures already generated"}

    teams = db.query(Team).all()

    team_ids = [team.id for team in teams]

    fixtures = generate_round_robin(team_ids)

    for fixture in fixtures:

        db_fixture = Fixture(
            home_team_id=fixture["home_team_id"],
            away_team_id=fixture["away_team_id"],
            matchday=fixture["matchday"]
        )

        db.add(db_fixture)

    db.commit()

    return {
        "message": "Fixtures generated successfully",
        "total_fixtures": len(fixtures)
    }

@routerFix.get("/fixtures")
def get_all_fixtures(db: Session = Depends(get_db)):
    fixtures = db.query(Fixture).all()
    return fixtures


@routerFix.get("/fixtures/{id}")
def get_matchday_fixtures(id: int, db: Session = Depends(get_db)):

    fixtures = (
        db.query(Fixture)
        .filter(Fixture.matchday == id)
        .all()
    )

    result = []

    for f in fixtures:
        result.append({
            "matchday": f.matchday,
            "home_team": f.home_team_id,
            "away_team": f.away_team_id,
            "home_score": f.home_score,
            "away_score": f.away_score,
            "status": f.status
        })

    return result

@routerFix.post("/simulate/match/{fixture_id}")
def simulate_single_match(fixture_id: int, db: Session = Depends(get_db)):

    fixture = db.query(Fixture).filter(Fixture.id == fixture_id).first()

    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    home_team = db.query(Team).get(fixture.home_team_id)
    away_team = db.query(Team).get(fixture.away_team_id)

    home_score, away_score = simulate_match(
        home_team.rating,
        away_team.rating
    )

    fixture.home_score = home_score
    fixture.away_score = away_score
    fixture.status = "played"

    db.commit()

    return {
        "home_team": home_team.name,
        "away_team": away_team.name,
        "score": f"{home_score} - {away_score}"
    }

@routerFix.post("/simulate/matchday/{week}")
def simulate_matchday(week: int, db: Session = Depends(get_db)):

    fixtures = db.query(Fixture)\
        .filter(Fixture.matchday == week)\
        .all()

    results = []

    for fixture in fixtures:

        home_team = db.query(Team).get(fixture.home_team_id)
        away_team = db.query(Team).get(fixture.away_team_id)

        # simulate score
        home_score, away_score = simulate_match(
            home_team.rating,
            away_team.rating
        )

        # update fixture
        fixture.home_score = home_score
        fixture.away_score = away_score
        fixture.status = "played"

        # get team stats
        home_stats = db.query(TeamStats)\
            .filter(TeamStats.team_id == home_team.id)\
            .first()

        away_stats = db.query(TeamStats)\
            .filter(TeamStats.team_id == away_team.id)\
            .first()

        # update standings
        update_team_stats(home_stats, away_stats, home_score, away_score)

        results.append({
            "home_team": home_team.name,
            "away_team": away_team.name,
            "score": f"{home_score}-{away_score}"
        })

    db.commit()

    return {
        "matchday": week,
        "results": results
    }

@routerFix.get("/table")
def getStandings(db: Session = Depends(get_db)):
    table = db.query(TeamStats).all()
    return table
    

@routerFix.post("/initialize-stats")
def initialize_stats(db: Session = Depends(get_db)):

    teams = db.query(Team).all()

    for team in teams:

        existing = db.query(TeamStats).filter(
            TeamStats.team_id == team.id
        ).first()

        if not existing:
            stats = TeamStats(team_id=team.id)
            db.add(stats)

    db.commit()

    return {"message": "Team stats initialized"}