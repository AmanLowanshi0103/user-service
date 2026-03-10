from fastapi import FastAPI, Depends, APIRouter
from app.model import models
from app.database.database import engine, SessionLocal
from app.router.userRouter import router   

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="User Service")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "FastAPI project running"}