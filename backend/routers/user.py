import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from db.database import get_db
from models.user import User
from schemas.user import UserRegisterRequest, UserResponse, UserLoginRequest, TokenResponse
from core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def hash_password(password: str) -> str:
    """
    Criptografa a senha usando bcrypt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha corresponde ao hash
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um token JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar um novo usuário
    """
    # Verificar se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    
    # Validar o tamanho da senha
    if len(request.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="A senha deve ter pelo menos 6 caracteres"
        )
    
    # Criar novo usuário com senha criptografada
    hashed_pwd = hash_password(request.password)
    new_user = User(
        email=request.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para login de usuário
    Retorna um JWT token se as credenciais forem válidas
    """
    # Buscar usuário pelo email
    user = db.query(User).filter(User.email == request.email).first()
    
    # Verificar se o usuário existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Verificar a senha
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Criar token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
