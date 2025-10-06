# 🏗️ Guia de Arquitetura do Backend

## 📚 Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura de Pastas](#estrutura-de-pastas)
3. [Fluxo de Dados](#fluxo-de-dados)
4. [Componentes Principais](#componentes-principais)
5. [Exemplo Prático: Criando uma História](#exemplo-prático)
6. [Exemplo Prático: Login de Usuário](#exemplo-prático-login)
7. [Como Adicionar uma Nova Feature](#como-adicionar-nova-feature)

---

## 🎯 Visão Geral

Este backend é construído com **FastAPI** e segue uma arquitetura em camadas bem definida. Pense nele como uma fábrica organizada:

```
Cliente (Frontend) 
    ↓
🚪 Router (Recebe pedidos)
    ↓
📋 Schema (Valida os dados)
    ↓
💼 Lógica de Negócio (Processa)
    ↓
🗄️ Model (Salva no banco)
    ↓
✅ Resposta para o Cliente
```

---

## 📁 Estrutura de Pastas

```
backend/
│
├── main.py                    # 🚀 Ponto de entrada da aplicação
│
├── core/                      # 🧠 Coração da aplicação
│   ├── config.py             # ⚙️ Configurações (API keys, DB, etc)
│   ├── prompts.py            # 💬 Prompts para IA
│   ├── story_generator.py    # 🤖 Gerador de histórias com IA
│   └── models.py             # 📊 Modelos de dados para IA
│
├── db/                        # 🗄️ Banco de dados
│   └── database.py           # 🔌 Conexão e sessão do banco
│
├── models/                    # 📦 Modelos SQLAlchemy (tabelas)
│   ├── user.py               # 👤 Tabela de usuários
│   ├── story.py              # 📖 Tabela de histórias
│   └── job.py                # 💼 Tabela de jobs assíncronos
│
├── schemas/                   # 📋 Validação de dados (Pydantic)
│   ├── user.py               # Schemas de usuário
│   ├── story.py              # Schemas de história
│   └── job.py                # Schemas de job
│
├── routers/                   # 🚪 Endpoints da API
│   ├── user.py               # Rotas de autenticação
│   ├── story.py              # Rotas de histórias
│   └── job.py                # Rotas de jobs
│
├── alembic/                   # 🔄 Migrações de banco de dados
│   └── versions/             # Histórico de mudanças no schema
│
├── .env                       # 🔐 Variáveis de ambiente (NÃO COMMITAR!)
├── .env.example              # 📝 Template de variáveis
├── requirements.txt          # 📦 Dependências Python
└── databse.db               # 💾 Banco SQLite (desenvolvimento)
```

---

## 🔄 Fluxo de Dados

### 1️⃣ Requisição HTTP chega ao servidor

```
POST /api/stories/create
Body: { "theme": "medieval fantasy" }
```

### 2️⃣ Router recebe e direciona

```python
# routers/story.py
@router.post("/stories/create")
def create_story(request: StoryCreateRequest):
    # Este endpoint é chamado
```

### 3️⃣ Schema valida os dados

```python
# schemas/story.py
class StoryCreateRequest(BaseModel):
    theme: str  # Pydantic valida que theme é uma string
```

### 4️⃣ Lógica de negócio processa

```python
# core/story_generator.py
generator = StoryGenerator()
story = generator.generate_story(theme)
```

### 5️⃣ Model salva no banco

```python
# models/story.py
new_story = Story(title=title, theme=theme)
db.add(new_story)
db.commit()
```

### 6️⃣ Resposta retorna ao cliente

```json
{
  "story_id": 1,
  "title": "The Dragon's Quest",
  "session_id": "abc-123"
}
```

---

## 🧩 Componentes Principais

### 🚀 `main.py` - O Maestro

O arquivo `main.py` é o ponto de entrada. Ele:

```python
from fastapi import FastAPI
from routers import story, job, user

app = FastAPI()  # Cria a aplicação

# Registra os routers (grupos de rotas)
app.include_router(story.router, prefix="/api")
app.include_router(job.router, prefix="/api")
app.include_router(user.router, prefix="/api")
```

**Analogia:** É como o gerente de um restaurante que organiza as diferentes áreas (cozinha, atendimento, caixa).

---

### 🚪 `routers/` - As Portas de Entrada

Cada arquivo em `routers/` define um conjunto de endpoints relacionados.

**Exemplo: `routers/story.py`**

```python
from fastapi import APIRouter

router = APIRouter(prefix="/stories", tags=["stories"])

@router.post("/create")
def create_story(request: StoryCreateRequest):
    # Lógica aqui
    return {"story_id": 1}

@router.get("/{story_id}/complete")
def get_story(story_id: int):
    # Buscar história no banco
    return story
```

**Rotas disponíveis:**
- `POST /api/stories/create` → Criar história
- `GET /api/stories/{id}/complete` → Buscar história completa

**Analogia:** São os garçons que recebem os pedidos dos clientes.

---

### 📋 `schemas/` - Os Validadores

Schemas definem a estrutura dos dados usando **Pydantic**.

**Exemplo: `schemas/story.py`**

```python
from pydantic import BaseModel

class StoryCreateRequest(BaseModel):
    theme: str  # Campo obrigatório

class StoryResponse(BaseModel):
    id: int
    title: str
    session_id: str
    
    class Config:
        from_attributes = True  # Permite converter de SQLAlchemy
```

**Função:**
- ✅ Valida dados de entrada
- ✅ Define formato de saída
- ✅ Gera documentação automática

**Analogia:** É o cardápio que diz exatamente o que o cliente pode pedir e o que vai receber.

---

### 🗄️ `models/` - As Tabelas do Banco

Models definem a estrutura das tabelas usando **SQLAlchemy**.

**Exemplo: `models/story.py`**

```python
from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relacionamento
    nodes = relationship("StoryNode", back_populates="story")
```

**SQL Equivalente:**
```sql
CREATE TABLE stories (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    session_id VARCHAR,
    created_at DATETIME
);
```

**Analogia:** É o arquivo de estoque do restaurante que registra tudo o que entra e sai.

---

### 🧠 `core/` - O Cérebro

Contém a lógica de negócio principal.

#### `core/config.py` - Configurações

```python
class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SECRET_KEY: str  # Para JWT
    
    class Config:
        env_file = ".env"  # Lê do arquivo .env
```

**Carrega variáveis do `.env`:**
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./databse.db
```

#### `core/story_generator.py` - Gerador de Histórias

```python
class StoryGenerator:
    def generate_story(self, theme: str) -> dict:
        # 1. Cria prompt para IA
        prompt = f"Create a story about {theme}"
        
        # 2. Chama OpenAI via LangChain
        response = llm.invoke(prompt)
        
        # 3. Processa resposta
        story_data = parse_response(response)
        
        return story_data
```

**Fluxo:**
```
Tema → Prompt → OpenAI → JSON → Banco de Dados
```

---

### 🔌 `db/database.py` - Conexão com Banco

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cria engine (conexão)
engine = create_engine(settings.DATABASE_URL)

# Cria sessão
SessionLocal = sessionmaker(bind=engine)

# Função para obter sessão
def get_db():
    db = SessionLocal()
    try:
        yield db  # Fornece sessão
    finally:
        db.close()  # Fecha quando terminar
```

**Uso nos routers:**
```python
@router.post("/stories")
def create_story(db: Session = Depends(get_db)):
    story = Story(title="Test")
    db.add(story)
    db.commit()
```

**Analogia:** É a conexão com o armazém central. Cada requisição pega uma "carreta" (sessão) para buscar/entregar dados.

---

## 📖 Exemplo Prático: Criando uma História

Vamos seguir o fluxo completo de uma requisição:

### 1. Cliente faz requisição

```javascript
// Frontend
axios.post('/api/stories/create', {
  theme: 'space adventure'
})
```

### 2. Router recebe

```python
# routers/story.py
@router.post("/stories/create")
async def create_story(
    request: StoryCreateRequest,  # ← Schema valida
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)  # ← Sessão do banco
):
    # Gera ID único para a sessão
    session_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    
    # Cria job assíncrono
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )
    db.add(job)
    db.commit()
    
    # Inicia geração em background
    background_tasks.add_task(
        generate_story_background,
        job_id, request.theme, session_id
    )
    
    return {
        "session_id": session_id,
        "job_id": job_id
    }
```

### 3. Background task processa

```python
def generate_story_background(job_id, theme, session_id):
    db = SessionLocal()
    
    try:
        # Busca o job
        job = db.query(StoryJob).filter(
            StoryJob.job_id == job_id
        ).first()
        
        # Gera história com IA
        generator = StoryGenerator()
        story_data = generator.generate_story(theme)
        
        # Salva história
        story = Story(
            title=story_data['title'],
            session_id=session_id
        )
        db.add(story)
        db.commit()
        
        # Salva nós da história
        for node_data in story_data['nodes']:
            node = StoryNode(
                story_id=story.id,
                content=node_data['content'],
                is_root=node_data.get('is_root', False),
                options=node_data.get('options', [])
            )
            db.add(node)
        
        db.commit()
        
        # Atualiza job para completo
        job.status = "completed"
        job.story_id = story.id
        job.completed_at = datetime.utcnow()
        db.commit()
        
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()
    finally:
        db.close()
```

### 4. Cliente verifica status

```javascript
// Frontend faz polling
setInterval(() => {
  axios.get(`/api/jobs/${job_id}`)
    .then(res => {
      if (res.data.status === 'completed') {
        // Buscar história completa
        axios.get(`/api/stories/${story_id}/complete`)
      }
    })
}, 2000)
```

### 5. Buscar história completa

```python
# routers/story.py
@router.get("/{story_id}/complete")
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    # Busca história com todos os nós
    story = db.query(Story).filter(Story.id == story_id).first()
    
    if not story:
        raise HTTPException(status_code=404)
    
    # SQLAlchemy carrega automaticamente os relacionamentos
    return {
        "id": story.id,
        "title": story.title,
        "session_id": story.session_id,
        "nodes": [
            {
                "id": node.id,
                "content": node.content,
                "is_root": node.is_root,
                "is_ending": node.is_ending,
                "options": node.options
            }
            for node in story.nodes
        ]
    }
```

---

## 🔐 Exemplo Prático: Login de Usuário

### 1. Registro de Usuário

```python
# routers/user.py
@router.post("/auth/register")
def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    # 1. Verifica se email já existe
    existing = db.query(User).filter(
        User.email == request.email
    ).first()
    
    if existing:
        raise HTTPException(400, "Email já cadastrado")
    
    # 2. Criptografa senha com bcrypt
    hashed_password = hash_password(request.password)
    
    # 3. Cria usuário
    user = User(
        email=request.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    
    return user  # Schema converte para UserResponse
```

### 2. Login de Usuário

```python
# routers/user.py
@router.post("/auth/login")
def login_user(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    # 1. Busca usuário
    user = db.query(User).filter(
        User.email == request.email
    ).first()
    
    if not user:
        raise HTTPException(401, "Credenciais inválidas")
    
    # 2. Verifica senha
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(401, "Credenciais inválidas")
    
    # 3. Gera token JWT
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=30)
    )
    
    # 4. Retorna token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

### 3. JWT Token

```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    # Assina com chave secreta
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
```

**Token JWT contém:**
```json
{
  "sub": "user@email.com",
  "user_id": 123,
  "exp": 1696600000
}
```

---

## 🆕 Como Adicionar uma Nova Feature

### Exemplo: Adicionar Sistema de Favoritos

#### 1. Criar Model (Tabela)

```python
# models/favorite.py
from sqlalchemy import Column, Integer, ForeignKey
from db.database import Base

class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    story_id = Column(Integer, ForeignKey("stories.id"))
```

#### 2. Criar Schema (Validação)

```python
# schemas/favorite.py
from pydantic import BaseModel

class FavoriteCreateRequest(BaseModel):
    story_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    story_id: int
    
    class Config:
        from_attributes = True
```

#### 3. Criar Router (Endpoints)

```python
# routers/favorite.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/")
def add_favorite(
    request: FavoriteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Auth
):
    favorite = Favorite(
        user_id=current_user.id,
        story_id=request.story_id
    )
    db.add(favorite)
    db.commit()
    return favorite

@router.get("/")
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()
    return favorites
```

#### 4. Registrar no main.py

```python
# main.py
from routers import story, job, user, favorite

app.include_router(favorite.router, prefix="/api")
```

#### 5. Criar Migração

```bash
alembic revision --autogenerate -m "Add favorites table"
alembic upgrade head
```

---

## 🔍 Conceitos Importantes

### Dependency Injection

FastAPI usa **Depends()** para injetar dependências:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stories")
def list_stories(db: Session = Depends(get_db)):
    # db é automaticamente fornecido e fechado
    return db.query(Story).all()
```

### Background Tasks

Para operações demoradas (geração de história):

```python
@router.post("/stories")
async def create(background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_story)
    return {"status": "processing"}
```

### Relacionamentos SQLAlchemy

```python
class Story(Base):
    nodes = relationship("StoryNode", back_populates="story")

class StoryNode(Base):
    story = relationship("Story", back_populates="nodes")
```

Acesso automático:
```python
story = db.query(Story).first()
print(story.nodes)  # Lista todos os nós automaticamente
```

---

## 🎓 Resumo

**Fluxo de uma requisição:**

```
1. Cliente faz HTTP Request
   ↓
2. FastAPI recebe em Router
   ↓
3. Schema valida dados de entrada
   ↓
4. Dependency Injection fornece DB session
   ↓
5. Lógica de negócio processa
   ↓
6. Model interage com banco de dados
   ↓
7. Schema formata resposta
   ↓
8. FastAPI retorna HTTP Response
```

**Organização:**
- 🚪 **Routers** = Portas de entrada (HTTP endpoints)
- 📋 **Schemas** = Contratos de dados (validação)
- 🗄️ **Models** = Tabelas do banco (SQLAlchemy)
- 🧠 **Core** = Lógica de negócio (IA, processamento)
- 🔌 **DB** = Conexão com banco de dados

**Regra de Ouro:**
> Cada camada tem uma responsabilidade específica. Não misture lógica de negócio no router, nem acesso ao banco direto no core!

---

## 📚 Próximos Passos

1. ✅ Entender o fluxo de dados
2. ✅ Explorar um router específico
3. ✅ Modificar um schema existente
4. ✅ Adicionar um novo endpoint
5. ✅ Criar sua primeira feature completa

**Dica:** Comece lendo `routers/story.py` e siga o fluxo até o banco de dados!
