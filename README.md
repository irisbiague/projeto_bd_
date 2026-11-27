#  Sistema de Gestão de Catering — BD Projeto

**Grupo P5G8** · Universidade de Aveiro · Bases de Dados (2.º semestre)

| Aluno | MEC |
|---|---|
| Íris Biaguê | 119251 |
| Tiago Ferreira | 78106 |

---

##  Contexto do Projeto

Este projeto consiste no desenvolvimento de uma **base de dados relacional** e de uma **aplicação web** para a gestão de uma empresa de **Catering**.

O sistema centraliza e organiza toda a informação necessária para a planificação e execução de eventos, integrando:

-  **Gestão de Clientes** — registo, consulta e atualização de dados
-  **Gestão de Eventos** — agendamento, orçamentação e alocação de recursos
-  **Gestão de Staff** — empregados, funções e alocação por evento
-  **Gestão de Menus** — criação de menus com pratos, bebidas e ingredientes
-  **Gestão de Fornecedores** — controlo de stock e lotes com validades
-  **Gestão de Serviços** — serviços internos e externos subcontratados

A base de dados foi desenhada em **SQL Server** (T-SQL), seguindo a **3ª Forma Normal (3NF)**, com recurso a *Stored Procedures*, *Triggers*, *Views* e *Filtered Indexes* para garantir integridade, desempenho e rastreabilidade.

---

##  Estrutura do Repositório

```
projeto_bd_/
│
├── sql/                        # Scripts SQL (executar por ordem)
│   ├── 01_ddl.sql              # Criação das tabelas e schemas
│   ├── 02_sp_functions.sql     # Stored Procedures e funções UDF
│   ├── 03_triggers.sql         # Triggers de integridade
│   ├── 04_db_init.sql          # Dados iniciais (seed)
│   └── 05_any_other_matter.sql # Índices e otimizações
│
├── app/                        # Aplicação web (Flask + Python)
│   ├── app.py                  # Ponto de entrada da aplicação
│   ├── requirements.txt        # Dependências Python
│   ├── controllers/            # Rotas HTTP (blueprints Flask)
│   ├── services/               # Lógica de negócio
│   ├── db/                     # Camada de acesso à base de dados
│   ├── templates/              # Templates HTML (Jinja2)
│   └── static/                 # Ficheiros estáticos (CSS, JS)
│
├── front-eventos/              # Protótipo alternativo de frontend
├── imagens/                    # Diagramas DER e ER
├── screenshots/                # Capturas de ecrã da aplicação
├── slides.pdf                  # Apresentação do projeto
├── Gravação_demo.mp4           # Vídeo de demonstração
└── apft_submit.md              # Relatório de submissão
```

---

##  Pré-requisitos

Antes de começar, certifica-te que tens instalado:

- **SQL Server** (Express ou superior) com o serviço `SQLEXPRESS` em execução
- **ODBC Driver 18 for SQL Server** ([download](https://learn.microsoft.com/pt-pt/sql/connect/odbc/download-odbc-driver-for-sql-server))
- **Python 3.10+** ([download](https://www.python.org/downloads/))

---

##  Configurar a Base de Dados

Abre o **SQL Server Management Studio (SSMS)** ou outro cliente SQL e executa os scripts **por esta ordem**:

```sql
-- 1. Criar tabelas, schemas e constraints
-- Ficheiro: sql/01_ddl.sql

-- 2. Criar Stored Procedures e funções
-- Ficheiro: sql/02_sp_functions.sql

-- 3. Criar Triggers
-- Ficheiro: sql/03_triggers.sql

-- 4. Popular a base de dados com dados iniciais
-- Ficheiro: sql/04_db_init.sql

-- 5. Criar índices para otimização
-- Ficheiro: sql/05_any_other_matter.sql
```

> **Nota:** Os scripts assumem que a base de dados se chama `Projeto`. Podes criá-la manualmente antes de correr os scripts com:
> ```sql
> CREATE DATABASE Projeto;
> ```

---

##  Correr a Aplicação Web

### 1. Instalar dependências

Abre um terminal na pasta `app/` e executa:

```powershell
cd app
py -m pip install -r requirements.txt
```

### 2. Verificar a ligação à base de dados

A configuração da ligação encontra-se em `app/db/database.py`:

```python
SQL_SERVER_CONFIG = {
    'driver': '{ODBC Driver 18 for SQL Server}',
    'server': '.\\SQLEXPRESS',   # Ajusta se o teu servidor tiver outro nome
    'database': 'Projeto',
    'trusted_connection': 'yes', # Autenticação Windows
}
```

Altera os campos `server` e `database` conforme a tua configuração local, se necessário.

### 3. Iniciar o servidor Flask

```powershell
py app.py
```

A aplicação ficará disponível em: **http://localhost:5000**

---

##  Funcionalidades da Aplicação

| Página | Descrição |
|---|---|
| **Criar Evento** | Formulário para registar um novo evento, associando cliente, menu, staff e serviços |
| **Catálogo de Catering** | Gestão de pratos — criação, listagem e remoção (soft-delete) |
| **Gestão de Menus** | Composição de menus com entradas, pratos principais, sobremesas e bebidas |
| **Gestão de Stock** | Visualização do stock atual e registo de entrada de novos lotes |

---

##  Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Base de Dados | Microsoft SQL Server (T-SQL) |
| Backend | Python 3 · Flask · pyodbc |
| Frontend | HTML · CSS · JavaScript (Jinja2 templates) |

---

##  Documentação Adicional

- [Relatório do Projeto](apft_submit.md)
- [Diagrama DER](imagens/DER.png)
- [Esquema Relacional](imagens/ER.png)
- [Slides de Apresentação](slides.pdf)
- [Vídeo de Demonstração](Gravação_demo.mp4)
