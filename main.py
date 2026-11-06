







from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- أضف هذا السطر
from sqlalchemy.orm import Session
import models, database
from ai_services import verify_face_match, anti_cheat_behavior_check

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Noor Kumhawy API", version="1.0")

# <-- أضف هذا الجُزء للسماح بالاتصال من أي واجهة
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from ai_services import verify_face_match, anti_cheat_behavior_check

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Noor Kumhawy API", version="1.0")

@app.post("/api/register")
def register_user(national_id: str, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.national_id == national_id).first()
    if existing_user:
        return {"message": "User already registered", "user_id": existing_user.id}
    
    new_user = models.User(national_id=national_id, current_level=12, total_points=100)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registered successfully with 100 bonus points", "user_id": new_user.id}

@app.post("/api/verify-face")
def verify_face(user_id: int, db: Session = Depends(database.get_db)):
    is_match = verify_face_match("path_to_saved_image", "path_to_current_selfie")
    if not is_match:
        raise HTTPException(status_code=400, detail="Face verification failed")
    return {"status": "success", "message": "Identity verified successfully"}

@app.post("/api/submit-exam")
def submit_exam(user_id: int, time_taken: int, score: int, db: Session = Depends(database.get_db)):
    if not anti_cheat_behavior_check(time_taken, min_allowed_time=30):
        raise HTTPException(status_code=400, detail="Anti-cheat triggered: too fast")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.total_points += score
    db.commit()
    return {"message": "Score saved successfully", "total_points": user.total_points}