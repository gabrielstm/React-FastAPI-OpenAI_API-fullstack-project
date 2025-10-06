# 🗄️ Como Visualizar o Diagrama ER do Banco de Dados

Este guia mostra diferentes formas de visualizar o Modelo Entidade-Relacionamento do banco de dados.

---

## 🚀 Método Mais Rápido (Recomendado)

### 📊 Opção 1: dbdiagram.io (Melhor para Apresentações)

1. **Acesse:** https://dbdiagram.io
2. **Copie** todo o conteúdo do arquivo `schema.dbml`
3. **Cole** no editor online
4. **Visualize** o diagrama interativo instantaneamente!

**Recursos:**
- ✅ Diagrama interativo e visual
- ✅ Exporta para PNG, PDF, SQL
- ✅ Compartilha link público
- ✅ Zoom e navegação
- ✅ Mostra relacionamentos com setas

**Preview:**
```
┌─────────────┐
│    USERS    │───┐
└─────────────┘   │
                  │ (future)
┌─────────────┐   │
│   STORIES   │←──┘
└─────────────┘
      ↓ 1:N
┌─────────────┐
│ STORY_NODES │
└─────────────┘
```

**Screenshot de exemplo:**
![dbdiagram](https://user-images.githubusercontent.com/example.png)

---

### 🌐 Opção 2: Mermaid Live Editor (GitHub Compatible)

1. **Acesse:** https://mermaid.live
2. **Abra** o arquivo `DATABASE_SCHEMA.md`
3. **Copie** o código que está entre as marcações ```mermaid
4. **Cole** no editor Mermaid Live

**Recursos:**
- ✅ Funciona em GitHub/GitLab (renderiza automaticamente)
- ✅ Exporta para PNG/SVG
- ✅ Sintaxe simples
- ✅ Integra com Markdown

**Visualização no GitHub:**
O código Mermaid renderiza automaticamente quando você vê o arquivo `DATABASE_SCHEMA.md` no GitHub!

---

## 💻 Ferramentas Desktop

### 🔹 DBeaver (Recomendado para Desenvolvedores)

**Instalação:**
```bash
# Windows (via Chocolatey)
choco install dbeaver

# Ou baixe: https://dbeaver.io/download/
```

**Como usar:**
1. Abra DBeaver
2. Conecte ao banco: `databse.db`
3. Vá em **Database → ER Diagram**
4. Visualize o diagrama gerado automaticamente!

**Recursos:**
- ✅ Mostra dados reais das tabelas
- ✅ Gera diagrama automaticamente
- ✅ Editor SQL integrado
- ✅ Explora relacionamentos

---

### 🔹 VS Code (Para Desenvolvedores)

**Extensões necessárias:**

1. **Mermaid Preview**
   ```bash
   code --install-extension bierner.markdown-mermaid
   ```

2. **PlantUML**
   ```bash
   code --install-extension jebbs.plantuml
   ```

**Como usar:**
1. Abra `DATABASE_SCHEMA.md` no VS Code
2. Pressione `Ctrl+Shift+V` (Preview do Markdown)
3. O diagrama Mermaid será renderizado!

**Ou:**
1. Abra arquivo com código PlantUML
2. `Ctrl+Shift+P` → "PlantUML: Preview"

---

### 🔹 MySQL Workbench

**Instalação:**
```bash
# Download: https://dev.mysql.com/downloads/workbench/
```

**Como usar:**
1. Abra MySQL Workbench
2. **File → New Model**
3. **File → Import → Reverse Engineer SQL CREATE Script**
4. Selecione o arquivo `schema.sql`
5. Visualize o diagrama ER!

**Recursos:**
- ✅ Designer visual profissional
- ✅ Edição gráfica de tabelas
- ✅ Exporta para múltiplos formatos
- ✅ Forward/Reverse engineering

---

## 📱 Ferramentas Online Alternativas

### PlantUML Online
- **URL:** http://www.plantuml.com/plantuml/uml/
- **Arquivo:** Cole o código PlantUML do `DATABASE_SCHEMA.md`

### Draw.io / diagrams.net
- **URL:** https://app.diagrams.net
- **Método:** Importar SQL ou desenhar manualmente

### QuickDBD
- **URL:** https://www.quickdatabasediagrams.com
- **Método:** Usar sintaxe própria ou importar

---

## 🎨 Comparação de Ferramentas

| Ferramenta | Facilidade | Visual | Exportação | Interativo | Grátis |
|------------|-----------|--------|------------|------------|--------|
| **dbdiagram.io** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | PNG, PDF, SQL | ✅ | ✅ |
| **Mermaid Live** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | PNG, SVG | ✅ | ✅ |
| **DBeaver** | ⭐⭐⭐ | ⭐⭐⭐⭐ | PNG, PDF | ✅ | ✅ |
| **MySQL Workbench** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Vários | ✅ | ✅ |
| **VS Code** | ⭐⭐⭐⭐ | ⭐⭐⭐ | PNG | ❌ | ✅ |
| **PlantUML Online** | ⭐⭐⭐ | ⭐⭐⭐ | PNG, SVG | ❌ | ✅ |

---

## 📋 Arquivos Disponíveis

| Arquivo | Formato | Ferramenta | Descrição |
|---------|---------|------------|-----------|
| `schema.dbml` | DBML | dbdiagram.io | Melhor para visualização rápida |
| `DATABASE_SCHEMA.md` | Markdown | GitHub/VS Code | Documentação + Mermaid/PlantUML |
| `schema.sql` | SQL DDL | DBeaver/Workbench | Esquema completo + dados exemplo |

---

## 🎯 Recomendações por Caso de Uso

### 🎨 Para Apresentações
→ Use **dbdiagram.io** (exporta PNG de alta qualidade)

### 📖 Para Documentação
→ Use **Mermaid** no `DATABASE_SCHEMA.md` (renderiza no GitHub)

### 🔧 Para Desenvolvimento
→ Use **DBeaver** (conecta no banco real e mostra dados)

### 🏗️ Para Design de Schema
→ Use **MySQL Workbench** (editor visual completo)

### 👥 Para Compartilhar com Time
→ Use **dbdiagram.io** (gera link público)

---

## 🚀 Quick Start (1 Minuto)

```bash
# Passo 1: Abra o arquivo
code backend/schema.dbml

# Passo 2: Copie TODO o conteúdo (Ctrl+A, Ctrl+C)

# Passo 3: Acesse
https://dbdiagram.io

# Passo 4: Cole no editor (Ctrl+V)

# Passo 5: Boom! Diagrama pronto! 🎉
```

---

## 📸 Como Exportar o Diagrama

### De dbdiagram.io:
1. Clique em **Export** (canto superior direito)
2. Escolha formato:
   - **PNG** - Para apresentações (recomendado)
   - **PDF** - Para documentos
   - **SQL** - Para criar banco

### De DBeaver:
1. Com diagrama aberto, clique direito
2. **Export Diagram → Image**
3. Escolha formato (PNG, SVG, PDF)

### De VS Code (Mermaid):
1. Preview aberto (`Ctrl+Shift+V`)
2. Clique direito no diagrama
3. **Save as PNG/SVG**

---

## 🎓 Tutorial em Vídeo

### dbdiagram.io Tutorial:
```
1. Acesse https://dbdiagram.io
2. Clique em "+ New Diagram"
3. Delete o código de exemplo
4. Cole o conteúdo de schema.dbml
5. Pronto! Seu diagrama está pronto
```

**Dicas:**
- 🔍 Use **Zoom** (scroll do mouse)
- 🎨 Clique em **Settings** para mudar tema
- 📤 **Export** para salvar imagem
- 🔗 **Share** para gerar link público

---

## ❓ Troubleshooting

### "Não renderiza no GitHub"
→ Certifique-se de que está usando ```mermaid (com 3 backticks)

### "DBeaver não mostra diagrama"
→ Conecte ao banco primeiro, depois vá em Database → ER Diagram

### "PlantUML não funciona"
→ Instale Java: `choco install openjdk`

### "dbdiagram.io dá erro"
→ Verifique se copiou TODO o conteúdo do schema.dbml

---

## 🆘 Precisa de Ajuda?

**Problema com DBML?**
→ Veja a documentação: https://dbml.dbdiagram.io/docs

**Problema com Mermaid?**
→ Veja exemplos: https://mermaid.js.org/syntax/entityRelationshipDiagram.html

**Problema com PlantUML?**
→ Veja guia: https://plantuml.com/ie-diagram

---

## ✅ Checklist de Visualização

- [ ] Acessei dbdiagram.io
- [ ] Copiei schema.dbml
- [ ] Colei no editor
- [ ] Visualizei o diagrama
- [ ] (Opcional) Exportei para PNG
- [ ] (Opcional) Compartilhei link com time

---

## 🎉 Resultado Final

Você deve ver um diagrama mostrando:
- ✅ 4 tabelas (users, stories, story_nodes, story_jobs)
- ✅ Relacionamentos com setas
- ✅ Chaves primárias e estrangeiras
- ✅ Tipos de dados
- ✅ Índices

**Exemplo visual:**
```
USERS              STORIES           STORY_NODES
+----+            +----+            +----+
| id |            | id |←───────────| id |
|email|           |title|           |story_id|
|pass|            |session|         |content|
+----+            +----+            |is_root|
                     ↑              |options|
                     |              +----+
                     |
                  STORY_JOBS
                  +----+
                  | id |
                  |job_id|
                  |status|
                  |story_id|
                  +----+
```

---

**Escolha sua ferramenta favorita e visualize! 📊✨**
