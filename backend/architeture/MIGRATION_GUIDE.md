# 🔧 Guia de Resolução: Problema com Migrações Alembic

## ❌ Problema
As migrações do Alembic estão apagando dados ao invés de preservá-los.

## 🔍 Causa Raiz
1. **`create_tables()` no `main.py`** - conflita com Alembic
2. **Migrações mal geradas** - têm comandos DROP ao invés de ALTER/CREATE

## ✅ Solução Imediata

### Passo 1: Backup dos Dados (SEMPRE!)
```powershell
# Faça backup do banco de dados antes de qualquer migração
Copy-Item backend\databse.db backend\databse.db.backup
```

### Passo 2: Limpar Migrações Problemáticas

Se você já perdeu dados e quer recomeçar:

```powershell
cd backend

# 1. Deletar migrações problemáticas
Remove-Item alembic\versions\*.py

# 2. Resetar histórico do Alembic (se existir)
# Isso remove o controle de versão do banco
# ATENÇÃO: Só faça se quiser recomeçar do zero!
```

### Passo 3: Recriar Estrutura Corretamente

```powershell
# 1. Garantir que todos os models estão importados no Base
# Verifique que db/database.py importa todos os models

# 2. Criar migração inicial
alembic revision --autogenerate -m "Initial migration"

# 3. REVISAR a migração gerada em alembic/versions/
# Deve ter apenas CREATE TABLE, nunca DROP TABLE

# 4. Aplicar migração
alembic upgrade head
```

### Passo 4: Para Adicionar Nova Tabela (Users)

```powershell
# 1. Criar/modificar o model em models/user.py
# 2. Importar o model no __init__.py ou no alembic/env.py

# 3. Criar migração
alembic revision --autogenerate -m "Add users table"

# 4. SEMPRE revisar o arquivo gerado antes de aplicar!
# Deve ter:
#   op.create_table('users', ...)
# NÃO deve ter:
#   op.drop_table('stories')

# 5. Se estiver correto, aplicar
alembic upgrade head
```

## 📋 Checklist Antes de Aplicar Migração

- [ ] Fiz backup do banco de dados
- [ ] Removi `create_tables()` do `main.py`
- [ ] Revisei o arquivo de migração gerado
- [ ] A migração tem apenas os comandos esperados (CREATE/ALTER, não DROP)
- [ ] Testei em ambiente de desenvolvimento primeiro

## 🛠️ Comandos Úteis do Alembic

```powershell
# Ver versão atual do banco
alembic current

# Ver histórico de migrações
alembic history --verbose

# Reverter última migração
alembic downgrade -1

# Ir para versão específica
alembic upgrade <revision_id>

# Ver SQL que será executado (sem aplicar)
alembic upgrade head --sql
```

## 🔄 Fluxo Correto de Trabalho

1. **Desenvolver**: Modificar models SQLAlchemy
2. **Backup**: Copiar banco de dados
3. **Gerar**: `alembic revision --autogenerate -m "descrição"`
4. **Revisar**: Abrir arquivo gerado e verificar comandos
5. **Ajustar**: Editar migração se necessário
6. **Testar**: Aplicar em ambiente de teste
7. **Aplicar**: `alembic upgrade head`
8. **Verificar**: Testar aplicação e dados

## ⚠️ O Que NUNCA Fazer

- ❌ Usar `create_tables()` com Alembic ativo
- ❌ Aplicar migração sem revisar o arquivo gerado
- ❌ Fazer migração em produção sem backup
- ❌ Deletar manualmente tabelas quando usar Alembic
- ❌ Editar banco diretamente quando usar Alembic

## 🎯 Estrutura Correta para Alembic

### alembic/env.py deve ter:
```python
from db.database import Base
# Importar TODOS os models
from models.user import User
from models.story import Story
from models.job import StoryJob

target_metadata = Base.metadata
```

### main.py NÃO deve ter:
```python
create_tables()  # ❌ REMOVER ISSO
```

### Usar apenas:
```python
# As tabelas são criadas via:
alembic upgrade head
```

## 📝 Exemplo de Migração Correta (Adicionar Coluna)

```python
def upgrade() -> None:
    # ✅ CORRETO - adicionar coluna
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))

def downgrade() -> None:
    # ✅ CORRETO - remover coluna adicionada
    op.drop_column('users', 'phone')
```

## 📝 Exemplo de Migração INCORRETA

```python
def upgrade() -> None:
    # ❌ ERRADO - não deveria dropar tabelas existentes!
    op.drop_table('stories')
    op.drop_table('story_nodes')
```

---

**Lembre-se:** Alembic é para **evoluir** o schema, não recriá-lo do zero!
