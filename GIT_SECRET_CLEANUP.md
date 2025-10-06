# 🚨 GUIA: Remover Chave da OpenAI do Git

## ⚠️ AÇÃO URGENTE PRIMEIRO!

**A chave da OpenAI foi exposta publicamente!** Antes de continuar:

1. **Acesse:** https://platform.openai.com/api-keys
2. **Revogue/Delete** a chave que começa com `sk-proj-QYVHN4B3psuk8...`
3. **Crie uma nova chave**
4. **Atualize o arquivo `.env` local** com a nova chave

---

## 🔧 Solução: Limpar Histórico Git

### Opção 1: Reset e Refazer Commits (RECOMENDADO)

**Quando usar:** Se você ainda não fez push ou está trabalhando sozinho.

```powershell
# 1. Salvar alterações atuais (se houver)
git stash

# 2. Resetar para ANTES do commit problemático (9ee2e47)
git reset --hard 9ee2e47

# 3. Verificar que o .env não está no staged
git status

# 4. Adicionar .env ao .gitignore (se não estiver)
# Edite .gitignore e adicione:
# backend/.env

# 5. Fazer commit do .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"

# 6. Recuperar suas outras alterações
git stash pop
# OU refazer manualmente as mudanças dos commits perdidos

# 7. Fazer novos commits (SEM o .env)
git add .
git commit -m "feature/login implementation"

# 8. Force push (CUIDADO: só se ninguém mais usa esse branch)
git push origin localrun --force
```

---

### Opção 2: Rebase Interativo (Mais Controlado)

```powershell
# 1. Iniciar rebase interativo desde antes do commit problemático
git rebase -i 9ee2e47

# 2. No editor que abrir, você verá algo como:
#    pick 465386b fix/migrations
#    pick a739471 fix/migrations
#
# 3. Mude 'pick' para 'drop' no commit problemático:
#    drop 465386b fix/migrations
#    pick a739471 fix/migrations

# 4. Salve e feche o editor

# 5. Se houver conflitos, resolva e continue:
git rebase --continue

# 6. Force push
git push origin localrun --force
```

---

### Opção 3: Git Filter-Branch (Remove de TODO histórico)

**Quando usar:** Se o arquivo .env foi commitado várias vezes.

```powershell
# CUIDADO: Isso reescreve TODO o histórico!
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all

# Limpar referências
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin localrun --force
```

---

### Opção 4: BFG Repo Cleaner (Mais Rápido)

**Recomendado para projetos grandes.**

```powershell
# 1. Instalar BFG (requer Java)
# Download de: https://rtyley.github.io/bfg-repo-cleaner/

# 2. Fazer clone bare
git clone --mirror https://github.com/gabrielstm/React-FastAPI-OpenAI_API-fullstack-project.git

# 3. Executar BFG
java -jar bfg.jar --delete-files .env React-FastAPI-OpenAI_API-fullstack-project.git

# 4. Limpar e push
cd React-FastAPI-OpenAI_API-fullstack-project.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

---

## 📋 Checklist Pós-Limpeza

- [ ] Chave antiga da OpenAI foi revogada
- [ ] Nova chave foi gerada
- [ ] Arquivo `.env` atualizado com nova chave
- [ ] `.env` está no `.gitignore`
- [ ] Histórico git foi limpo
- [ ] Force push foi feito
- [ ] Verificar no GitHub que o `.env` não aparece mais

---

## 🛡️ Prevenção Futura

### 1. Sempre use .gitignore

Adicione ao `.gitignore` na raiz do projeto:
```
# Environment variables
.env
.env.local
.env.*.local
backend/.env
frontend/.env

# API Keys
*_key
*_secret
*.pem
```

### 2. Use Template .env

Crie um `.env.example` com valores fake:
```
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=sqlite:///./database.db
ALLOWED_ORIGINS=http://localhost:5173
```

### 3. Configure Git Hooks

```powershell
# Criar hook pre-commit
New-Item .git/hooks/pre-commit -Force

# Adicionar verificação
@"
#!/bin/sh
if git diff --cached --name-only | grep -q ".env"; then
    echo "ERROR: Attempting to commit .env file!"
    exit 1
fi
"@ | Set-Content .git/hooks/pre-commit

# Dar permissão de execução (no Git Bash)
chmod +x .git/hooks/pre-commit
```

### 4. Use GitHub Secrets (para CI/CD)

Para GitHub Actions, use Secrets ao invés de commitar chaves.

---

## ⚡ Comando Rápido (Se quiser fazer agora)

```powershell
# Resetar, limpar e refazer
cd C:\Users\gabriel\Documents\React-FastAPI-OpenAI_API-fullstack-project
git reset --hard 9ee2e47
echo "backend/.env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
# Refazer mudanças manualmente (login, migrations, etc)
git add .
git commit -m "Re-add features without .env"
git push origin localrun --force
```

---

**LEMBRE-SE:** 
1. ✅ Revogar chave antiga na OpenAI PRIMEIRO
2. ✅ Fazer backup antes de force push
3. ✅ Avisar colaboradores se houver
