from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Dict
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from models.story import Story
from models.job import StoryJob

router = APIRouter()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

# Simples token para exemplo
ADMIN_TOKEN = "admin-token-123"

@router.post("/admin/login")
def admin_login(data: Dict[str, str]):
    username = data.get("username")
    password = data.get("password")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"token": ADMIN_TOKEN}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

# Dependência para proteger rota

def verify_admin_token(request: Request):
    token = request.headers.get("Authorization")
    if token != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# Exemplo: retorna todos os dados do banco (ajustar para seu modelo real)
@router.get("/admin/data")
def get_all_data(dep=Depends(verify_admin_token), db: Session = Depends(get_db)):
    users = db.query(User).all()
    stories = db.query(Story).all()
    jobs = db.query(StoryJob).all()

    users_data = [
        {
            "id": u.id,
            "email": u.email,
            "profile_pic": u.profile_pic,
            "created_at": str(u.created_at)
        } for u in users
    ]
    stories_data = [
        {
            "id": s.id,
            "title": s.title,
            "session_id": s.session_id,
            "created_at": str(s.created_at)
        } for s in stories
    ]
    jobs_data = [
        {
            "id": j.id,
            "job_id": j.job_id,
            "session_id": j.session_id,
            "theme": j.theme,
            "status": j.status,
            "story_id": j.story_id,
            "error": j.error,
            "created_at": str(j.created_at),
            "completed_at": str(j.completed_at) if j.completed_at else None
        } for j in jobs
    ]
    return {
        "users": users_data,
        "stories": stories_data,
        "jobs": jobs_data
    }
