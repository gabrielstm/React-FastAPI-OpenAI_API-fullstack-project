# 📊 Diagramas e Fluxos do Backend

Este documento complementa o `ARCHITECTURE.md` com diagramas visuais e fluxogramas.

---

## 🗺️ Mapa Mental da Aplicação

```
                    🌐 FRONTEND
                         |
                         | HTTP Request
                         ↓
            ┌─────────────────────────┐
            │     FastAPI Server      │
            │      (main.py)          │
            └─────────────────────────┘
                         |
        ┌────────────────┼────────────────┐
        |                |                |
        ↓                ↓                ↓
    🚪 Stories       🚪 Jobs         🚪 Auth
    Router          Router          Router
        |                |                |
        ↓                ↓                ↓
    📋 Story         📋 Job          📋 User
    Schemas         Schemas         Schemas
        |                |                |
        └────────────────┼────────────────┘
                         ↓
                    🧠 Business Logic
                         ↓
                    🗄️ Database Layer
                         |
        ┌────────────────┼────────────────┐
        |                |                |
        ↓                ↓                ↓
    📦 Story         📦 Job          📦 User
    Model           Model           Model
        |                |                |
        └────────────────┼────────────────┘
                         ↓
                    💾 SQLite/PostgreSQL
```

---

## 🔄 Fluxo Completo: Criar História

### Diagrama de Sequência

```
Cliente          Router          Background       Generator       Database
  |                |                  |               |              |
  |--POST /create->|                  |               |              |
  |                |                  |               |              |
  |                |--Create Job----->|               |              |
  |                |                  |               |              |
  |                |------------------|-------------->|--Save Job--->|
  |                |                  |               |              |
  |<--job_id------|                  |               |              |
  |                |                  |               |              |
  |                |    start task    |               |              |
  |                |------------------->               |              |
  |                |                  |               |              |
  |                |                  |--generate---->|              |
  |                |                  |               |              |
  |                |                  |               |<--AI resp----|
  |                |                  |               |              |
  |                |                  |--Save Story-->|------------->|
  |                |                  |               |              |
  |                |                  |<--story_id----|              |
  |                |                  |               |              |
  |                |                  |--Update Job-->|------------->|
  |                |                  |               |              |
  |                |                  ✓               |              |
  |                |                                  |              |
  |--GET /jobs/{id}------------------>|               |              |
  |                |                  |               |              |
  |                |<-----------------|--Query Job----|------------->|
  |                |                  |               |              |
  |<--{status: completed}-------------|               |              |
  |                |                  |               |              |
  |--GET /stories/{id}----------------|               |              |
  |                |                  |               |              |
  |                |------------------|--Query Story--|------------->|
  |                |                  |               |              |
  |<--{story data}---------------------|               |              |
```

### Código Passo a Passo

**1. Cliente faz POST**
```http
POST /api/stories/create
Content-Type: application/json

{
  "theme": "medieval fantasy"
}
```

**2. Router recebe e valida**
```python
# routers/story.py
@router.post("/stories/create")
async def create_story(request: StoryCreateRequest):
    # Schema valida automaticamente
    # request.theme já está validado
```

**3. Cria Job no banco**
```python
job = StoryJob(
    job_id=str(uuid.uuid4()),      # "abc-123"
    session_id=str(uuid.uuid4()),  # "xyz-789"
    theme=request.theme,            # "medieval fantasy"
    status="pending"
)
db.add(job)
db.commit()
```

**4. Inicia tarefa em background**
```python
background_tasks.add_task(
    generate_story_background,
    job.job_id,
    request.theme,
    job.session_id
)

# Retorna imediatamente
return {
    "session_id": job.session_id,
    "job_id": job.job_id
}
```

**5. Background task gera história**
```python
# Roda em paralelo, não bloqueia
def generate_story_background(job_id, theme, session_id):
    # 1. Gera com IA
    generator = StoryGenerator()
    story_data = generator.generate_story(theme)
    
    # 2. Salva no banco
    story = Story(title=story_data['title'], ...)
    db.add(story)
    db.commit()
    
    # 3. Atualiza job
    job.status = "completed"
    job.story_id = story.id
    db.commit()
```

**6. Cliente verifica status (polling)**
```http
GET /api/jobs/{job_id}

Response:
{
  "status": "completed",
  "story_id": 1
}
```

**7. Cliente busca história completa**
```http
GET /api/stories/1/complete

Response:
{
  "id": 1,
  "title": "The Dragon's Quest",
  "nodes": [...]
}
```

---

## 🔐 Fluxo de Autenticação

### Diagrama de Autenticação

```
      REGISTRO                          LOGIN
         |                                |
         ↓                                ↓
    POST /register                   POST /login
         |                                |
         ↓                                ↓
    Valida dados                    Busca usuário
         |                                |
         ↓                                ↓
    Email existe?                   Usuário existe?
         |                                |
    Sim  |  Não                      Sim  |  Não
         ↓                                ↓
    ❌ Erro                          Verifica senha
         |                                |
         ↓                           ✓    |    ✗
    Hash senha                            ↓
         |                           Gera JWT    ❌ Erro
         ↓                                |
    Salva no DB                           ↓
         |                          Retorna token
         ↓
    ✅ Sucesso
```

### Código do Fluxo

**Registro:**
```python
# 1. Validação
class UserRegisterRequest(BaseModel):
    email: EmailStr      # Valida formato de email
    password: str        # Mínimo 6 caracteres

# 2. Router
@router.post("/auth/register")
def register(request: UserRegisterRequest, db: Session):
    # 3. Verifica se existe
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(400, "Email já existe")
    
    # 4. Hash da senha
    hashed = bcrypt.hashpw(
        request.password.encode('utf-8'),
        bcrypt.gensalt()
    )
    
    # 5. Salva
    user = User(email=request.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    
    return user
```

**Login:**
```python
@router.post("/auth/login")
def login(request: UserLoginRequest, db: Session):
    # 1. Busca usuário
    user = db.query(User).filter(
        User.email == request.email
    ).first()
    
    if not user:
        raise HTTPException(401, "Credenciais inválidas")
    
    # 2. Verifica senha
    if not bcrypt.checkpw(
        request.password.encode('utf-8'),
        user.hashed_password.encode('utf-8')
    ):
        raise HTTPException(401, "Credenciais inválidas")
    
    # 3. Gera JWT
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    
    token = jwt.encode(
        token_data,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    
    # 4. Retorna
    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

**Uso do Token:**
```python
# Cliente armazena token
localStorage.setItem('token', response.data.access_token)

# Cliente envia em requisições
headers: {
  'Authorization': 'Bearer ' + token
}

# Backend valida (futuro)
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.SECRET_KEY)
    return payload
```

---

## 🗄️ Estrutura do Banco de Dados

### Diagrama ER (Entity-Relationship)

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ hashed_password │
│ created_at      │
└─────────────────┘
         |
         | (future: user_id FK)
         |
┌─────────────────┐          ┌─────────────────┐
│    STORIES      │──────────│   STORY_NODES   │
├─────────────────┤   1:N    ├─────────────────┤
│ id (PK)         │<────────┐│ id (PK)         │
│ title           │         ││ story_id (FK)   │
│ session_id      │         ││ content         │
│ created_at      │         ││ is_root         │
└─────────────────┘         ││ is_ending       │
         |                  ││ options (JSON)  │
         |                  │└─────────────────┘
         |                  │
         | 1:1              │
         |                  │
┌─────────────────┐         │
│   STORY_JOBS    │         │
├─────────────────┤         │
│ id (PK)         │         │
│ job_id          │         │
│ session_id      │         │
│ theme           │         │
│ status          │         │
│ story_id (FK)   │─────────┘
│ error           │
│ created_at      │
│ completed_at    │
└─────────────────┘
```

### Relacionamentos

**1. Story → StoryNodes (1:N)**
```python
# models/story.py
class Story(Base):
    nodes = relationship("StoryNode", back_populates="story")

# models/story.py
class StoryNode(Base):
    story_id = Column(Integer, ForeignKey("stories.id"))
    story = relationship("Story", back_populates="nodes")
```

**Uso:**
```python
story = db.query(Story).first()
print(story.nodes)  # Lista todos os nós automaticamente
```

**2. StoryJob → Story (1:1)**
```python
# models/job.py
class StoryJob(Base):
    story_id = Column(Integer, ForeignKey("stories.id"))
```

---

## 📦 Ciclo de Vida de uma Sessão de Banco

```
1. Request chega
      ↓
2. Depends(get_db) cria sessão
      ↓
3. Sessão é passada para função
      ↓
4. Operações são feitas (query, add, update)
      ↓
5. db.commit() salva mudanças
      ↓
6. Função retorna
      ↓
7. finally: db.close() fecha sessão
```

**Código:**
```python
def get_db():
    db = SessionLocal()  # 2. Cria
    try:
        yield db         # 3. Passa
    finally:
        db.close()       # 7. Fecha

@router.get("/stories")
def list_stories(db: Session = Depends(get_db)):
    stories = db.query(Story).all()  # 4. Usa
    return stories                    # 6. Retorna
```

---

## 🎯 Padrões de Código

### Pattern: Repository-like

```python
# ✅ BOM - Lógica no router
@router.post("/stories")
def create_story(request: StoryCreateRequest, db: Session):
    story = Story(**request.dict())
    db.add(story)
    db.commit()
    return story

# ❌ EVITAR - Lógica complexa no router
@router.post("/stories")
def create_story(...):
    # 50 linhas de lógica complexa
    # Dificulta testes e reutilização
```

### Pattern: Dependency Injection

```python
# ✅ BOM - Usa Depends
@router.get("/stories")
def list_stories(
    db: Session = Depends(get_db),
    limit: int = 10
):
    return db.query(Story).limit(limit).all()

# ❌ EVITAR - Criar sessão manual
@router.get("/stories")
def list_stories():
    db = SessionLocal()  # Não fecha automaticamente!
    return db.query(Story).all()
```

### Pattern: Schema Conversion

```python
# ✅ BOM - Usa schema para resposta
@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    return user  # FastAPI converte automaticamente

# ❌ EVITAR - Retorna model direto sem schema
@router.get("/users/{id}")
def get_user(id: int, db: Session):
    return db.query(User).first()  # Expõe hashed_password!
```

---

## 🚀 Performance Tips

### 1. Eager Loading (Evita N+1 queries)

```python
# ❌ RUIM - N+1 problema
stories = db.query(Story).all()
for story in stories:
    print(story.nodes)  # Cada iteração faz 1 query!

# ✅ BOM - Carrega tudo de uma vez
from sqlalchemy.orm import joinedload

stories = db.query(Story).options(
    joinedload(Story.nodes)
).all()
for story in stories:
    print(story.nodes)  # Sem queries extras!
```

### 2. Índices

```python
# models/story.py
class Story(Base):
    session_id = Column(String, index=True)  # ✅ Índice para buscas rápidas
```

### 3. Background Tasks

```python
# ✅ BOM - Operação demorada em background
background_tasks.add_task(send_email, user.email)
return {"status": "processing"}

# ❌ RUIM - Bloqueia resposta
send_email(user.email)  # Cliente espera 5 segundos
return {"status": "sent"}
```

---

## 🔍 Debugging Tips

### 1. Logs SQL

```python
# Adicione ao .env
DATABASE_URL=sqlite:///./databse.db?echo=True

# Ou no código
engine = create_engine(url, echo=True)  # Mostra todas as queries
```

### 2. Pydantic Validation Errors

```python
try:
    story = StoryCreateRequest(**data)
except ValidationError as e:
    print(e.json())  # Mostra exatamente o que falhou
```

### 3. FastAPI Docs

```
http://localhost:8000/docs
```
- ✅ Testa endpoints interativamente
- ✅ Vê schemas automáticos
- ✅ Testa com dados reais

---

## 📚 Glossário

- **Router**: Grupo de endpoints relacionados
- **Schema**: Validação de dados com Pydantic
- **Model**: Definição de tabela com SQLAlchemy
- **Session**: Conexão temporária com banco
- **Dependency Injection**: FastAPI fornece automaticamente
- **Background Task**: Tarefa executada após resposta
- **Migration**: Mudança no schema do banco
- **JWT**: Token de autenticação
- **CORS**: Permite requisições de outros domínios
- **ORM**: Object-Relational Mapping (SQLAlchemy)

---

## 🎓 Exercícios Práticos

### Exercício 1: Adicionar Campo
Adicione um campo `description` na tabela `stories`.

**Passos:**
1. Modificar `models/story.py`
2. Modificar `schemas/story.py`
3. Criar migração: `alembic revision --autogenerate -m "add description"`
4. Aplicar: `alembic upgrade head`

### Exercício 2: Novo Endpoint
Crie `GET /api/stories/recent` que retorna as 5 histórias mais recentes.

**Dica:**
```python
@router.get("/stories/recent")
def get_recent_stories(db: Session = Depends(get_db)):
    return db.query(Story).order_by(
        Story.created_at.desc()
    ).limit(5).all()
```

### Exercício 3: Relacionamento
Adicione relação `User → Stories` (um usuário tem várias histórias).

**Dica:**
```python
class Story(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="stories")
```

---

**Próximo:** Leia `ARCHITECTURE.md` para entender conceitos em detalhes!
