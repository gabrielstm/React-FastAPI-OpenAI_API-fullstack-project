import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os
import shutil
import uuid

from db.database import get_db
from models.user import User
from schemas.user import UserRegisterRequest, UserResponse, UserLoginRequest, TokenResponse
from core.config import settings
from core.redis_client import redis_client

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


def get_current_user(credentials: HTTPBearer = Depends(HTTPBearer()), db: Session = Depends(get_db)):
    """
    Dependência para obter o usuário atual a partir do token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if email is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    email: str = Form(...),
    password: str = Form(...),
    profile_pic: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar um novo usuário
    """
    # Verificar se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    
    # Validar o tamanho da senha
    if len(password) < 6:
        raise HTTPException(
            status_code=400,
            detail="A senha deve ter pelo menos 6 caracteres"
        )
    
    profile_pic_path = None
    if profile_pic:
        # Criar diretório uploads se não existir
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # Gerar nome único para o arquivo
        file_extension = os.path.splitext(profile_pic.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Salvar o arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_pic.file, buffer)

        # Salvar o caminho com barra inicial para servir corretamente
        profile_pic_path = f"/uploads/{unique_filename}"
    
    # Criar novo usuário com senha criptografada
    hashed_pwd = hash_password(password)
    new_user = User(
        email=email,
        hashed_password=hashed_pwd,
        profile_pic=profile_pic_path
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


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint para obter os dados do usuário atual
    """
    # Tenta buscar foto de perfil do cache Redis
    profile_pic = current_user.profile_pic
    try:
        cache_key = f"user_profile_pic:{current_user.id}"
        cached_pic = redis_client.get(cache_key)
        if cached_pic is not None:
            profile_pic = cached_pic
        else:
            # Se não estiver no cache, salva no Redis
            if profile_pic:
                redis_client.set(cache_key, profile_pic)
    except Exception:
        # Se Redis falhar, usa o valor do banco
        pass
    
    # Retorna o usuário
    return {
        "id": current_user.id,
        "email": current_user.email,
        "profile_pic": profile_pic,
        "created_at": current_user.created_at
    }
