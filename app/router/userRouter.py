from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.userschemas import userData,UserUpdate
from app.model.models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/user")

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/create")
def createUser(userData : userData, db: Session=Depends(get_db)):
    user=User(name=userData.name, password=userData.password, email=userData.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    
@router.get("/alluser")
def getAllUser(db: Session=Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{id}")
def getOneUser(id:int, db: Session=Depends(get_db)):
    user= db.query(User).filter(User.id==id).first()
    return user

@router.delete("/{id}")
def deleteUser(id:int, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    db.delete(user)
    db.commit()
    return user

@router.put("/{id}")
def update_user(id: int, user_update: UserUpdate , db: Session = Depends(get_db)):
    # Fetch the user
    user = db.query(User).filter(User.id == id).first()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = user_update.password  # Ideally hash passwords
    
    db.commit()
    db.refresh(user)  # Refresh to get updated data
    
    return {"message": "User updated successfully", "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }}