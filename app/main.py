from fastapi import FastAPI, Depends, APIRouter
from app.model import models
from app.database.database import engine, SessionLocal
from app.router.userRouter import router   
from app.router.teamsRouter import routerTeams
from app.router.fixturesRouter import routerFix
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="User Service")

app.include_router(router)
app.include_router(routerTeams)
app.include_router(routerFix)

origins = [
    "http://localhost:5173",
]

# Add the middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only specified origins
    allow_credentials=True, # Allows cookies/authentication
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

@app.get("/")
def root():
    return {"message": "FastAPI project running"}

