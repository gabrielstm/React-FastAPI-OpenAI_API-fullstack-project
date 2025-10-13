from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from core.config import settings
from routers import story, job, user
from routers import admin

# Não usar create_tables() quando estiver usando Alembic
# As tabelas devem ser criadas via migrações: alembic upgrade head

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretório uploads se não existir
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)
app.include_router(user.router, prefix=settings.API_PREFIX)
app.include_router(admin.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "hello world"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)