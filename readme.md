# 📖 Interactive Story Generator

Uma aplicação fullstack para criar histórias interativas do tipo "Choose Your Own Adventure" usando inteligência artificial. Os usuários podem escolher um tema e a IA gera uma história com múltiplas escolhas e caminhos diferentes.

## ✨ Características

- 🤖 **Geração de histórias com IA** usando OpenAI GPT-4o-mini via LangChain
- 🎮 **Narrativa interativa** com múltiplas escolhas e finais diferentes
- ⚡ **Processamento assíncrono** com sistema de jobs para geração de histórias
- 🗄️ **Persistência de dados** com SQLite e SQLAlchemy
- 🎨 **Interface moderna** construída com React + Vite
- 🔄 **API RESTful** com FastAPI
- 📝 **Documentação automática** com Swagger/OpenAPI

## 🏗️ Arquitetura

```
.
├── backend/          # FastAPI + Python
│   ├── core/        # Lógica de negócio e geração de histórias
│   ├── db/          # Configuração do banco de dados
│   ├── models/      # Modelos SQLAlchemy
│   ├── routers/     # Endpoints da API
│   └── schemas/     # Schemas Pydantic
└── frontend/         # React + Vite
    └── src/
        └── components/  # Componentes React
```

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **LangChain** - Framework para aplicações com LLMs
- **OpenAI API** - GPT-4o-mini para geração de histórias
- **Uvicorn** - Servidor ASGI
- **Python 3.12+**

### Frontend
- **React 19** - Biblioteca UI
- **Vite** - Build tool e dev server
- **React Router** - Navegação
- **Axios** - Cliente HTTP
- **ESLint** - Linter

## 📋 Pré-requisitos

- Python 3.13 ou superior
- Node.js 18 ou superior
- npm ou yarn
- Conta OpenAI com chave API

## ⚙️ Instalação

### Backend

1. Navegue até o diretório do backend:
```powershell
cd backend
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Instale as dependências:
```powershell
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente criando um arquivo `.env`:
```env
OPENAI_API_KEY=sua_chave_api_aqui
ALLOWED_ORIGINS=http://localhost:5173
```

5. Inicie o servidor:
```powershell
uv run .\main.py
```

5.1 Caso instale algum pacote:
```powershell
uv sync
```


6. migrações
```powershell
alembic init alembic
```

6.1 criar uma migração
```powershell
alembic revision --autogenerate -m "Users Table"
```

6.2 executar uma migração
```powershell
alembic upgrade head
```

O backend estará disponível em `http://localhost:8000`

**Documentação da API:** `http://localhost:8000/docs`

### Frontend

1. Navegue até o diretório do frontend:
```powershell
cd frontend
```

2. Instale as dependências:
```powershell
npm install
```

3. Crie um arquivo `.env` (se necessário):
```env
VITE_API_URL=http://localhost:8000
```

4. Inicie o servidor de desenvolvimento:
```powershell
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## 🎮 Como Usar

1. Acesse a aplicação em `http://localhost:5173`
2. Digite um tema para sua história (ex: "fantasia medieval", "ficção científica", "mistério")
3. Clique em "Gerar História"
4. Aguarde enquanto a IA cria sua história personalizada
5. Leia a história e escolha entre as opções apresentadas
6. Explore diferentes caminhos e finais!

## 📡 Endpoints da API

### Stories

- `POST /api/v1/stories/generate` - Inicia a geração de uma nova história
  - Body: `{ "theme": "fantasy" }`
  - Retorna: `{ "session_id": "uuid", "job_id": "uuid" }`

- `GET /api/v1/stories/{session_id}` - Busca uma história gerada
  - Retorna: Objeto Story completo com nós e opções

### Jobs

- `GET /api/v1/jobs/{job_id}` - Verifica o status de um job de geração
  - Retorna: Status do job (pending, completed, failed)

## 🗄️ Estrutura do Banco de Dados

### Story
- `id`: UUID único
- `theme`: Tema da história
- `title`: Título gerado
- `session_id`: ID da sessão
- `created_at`: Data de criação

### StoryNode
- `id`: UUID único
- `story_id`: Referência à história
- `content`: Conteúdo do nó
- `node_type`: Tipo (start, choice, ending)
- `choices`: Opções disponíveis (JSON)

### Job
- `id`: UUID único
- `session_id`: ID da sessão
- `status`: Status do job
- `created_at`: Data de criação
- `completed_at`: Data de conclusão

## 🔧 Scripts Disponíveis

### Backend
```powershell
python main.py        # Inicia o servidor em modo desenvolvimento
```

### Frontend
```powershell
npm run dev          # Servidor de desenvolvimento
npm run build        # Build de produção
npm run preview      # Preview do build
npm run lint         # Executa o linter
```

## 🌟 Funcionalidades Futuras

- [ ] Suporte a múltiplos idiomas
- [ ] Sistema de salvamento de histórias favoritas
- [ ] Compartilhamento de histórias
- [ ] Customização de personagens
- [ ] Temas pré-definidos
- [ ] Exportação de histórias em PDF
- [ ] Sistema de autenticação de usuários

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

