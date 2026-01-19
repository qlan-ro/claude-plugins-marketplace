# AI Tooling Registry

This file serves as the local registry of available skills, agents, and MCP servers.
In production, this will be fetched dynamically from providers like `skillsmp.com` or `aitmpl.com`.

## Registry Providers

| Provider | URL | Type |
|----------|-----|------|
| SkillsMP | https://skillsmp.com | Skills marketplace |
| AITemplates | https://aitmpl.com | Skills & agents |
| MCP Registry | https://mcp-registry.anthropic.com | MCP servers |
| Claude Default | Built-in | Default skills |

## How to Use This Registry

When configuring AI workflow (Phase 2), query this registry to find matching tools:

1. **Classify project** by tech stack and features
2. **Query registry** for matching skills/agents/MCP servers
3. **Present options** to user with sources and descriptions
4. **Generate config** with selected tools

---

## Skills Registry

### Claude Default Skills (Always Available)

| Skill ID | Name | Purpose | Trigger Keywords |
|----------|------|---------|------------------|
| `docx` | Word Documents | Create, edit, analyze .docx files | document, word, report, letter |
| `pdf` | PDF Processing | Extract, create, merge PDFs | pdf, form, extract |
| `pptx` | PowerPoint | Create, edit presentations | presentation, slides, deck |
| `xlsx` | Excel | Spreadsheets, data analysis | spreadsheet, excel, data table |
| `frontend-design` | Frontend Design | Production-grade UI/UX | ui, ux, design, frontend |
| `web-artifacts-builder` | Web Components | React/Tailwind/shadcn | react, component, tailwind |
| `webapp-testing` | Web Testing | Playwright UI testing | test, e2e, playwright |
| `skill-creator` | Skill Creator | Create new skills | create skill, new skill |

### External Skills (skillsmp.com)

| Skill ID | Name | Source URL | Tech Stack | Keywords |
|----------|------|------------|------------|----------|
| `database-implementation` | Database Design | [skillsmp.com](https://skillsmp.com/skills/jpicklyk-task-orchestrator-claude-plugins-task-orchestrator-skills-database-implementation-skill-md) | SQL, Schema | database, schema, tables |
| `postgresql` | PostgreSQL | [skillsmp.com](https://skillsmp.com/skills/2025emma-vibe-coding-cn-i18n-zh-skills-postgresql-skill-md) | PostgreSQL | postgres, postgresql |
| `sqlserver` | SQL Server | [skillsmp.com](https://skillsmp.com/skills/fabriciofs-mcp-sql-server-claude-skills-sqlserver-expert-skill-md) | SQL Server | sqlserver, mssql |
| `sql-review` | SQL Review | [skillsmp.com](https://skillsmp.com/skills/hubert-dudek-medium-news-202602-skills-sql-performance-review-skill-md) | SQL | sql review, performance |
| `flyway-migrations` | Flyway Migrations | [skillsmp.com](https://skillsmp.com/skills/navikt-copilot-github-skills-flyway-migration-skill-md) | Java, Flyway | migration, flyway, database |
| `oracle-sql` | Oracle SQL | [skillsmp.com](https://skillsmp.com/skills/acedergren-oracle-dba-skill-skill-md) | Oracle | oracle, plsql |
| `databricks-sql-converter` | SQL Converter | [skillsmp.com](https://skillsmp.com/skills/sfc-gh-dflippo-snowflake-dbt-demo-claude-skills-dbt-migration-skill-md) | Databricks, dbt | convert, migrate, databricks |
| `jupyter-notebook` | Jupyter | [skillsmp.com](https://skillsmp.com/skills/i9wa4-dotfiles-config-claude-skills-jupyter-notebook-skill-md) | Python, Jupyter | notebook, jupyter, data science |
| `python-dev` | Python Development | [skillsmp.com](https://skillsmp.com/skills/databricks-solutions-ai-dev-kit-claude-skills-python-dev-skill-md) | Python | python, pip, venv |
| `fastapi` | FastAPI | [skillsmp.com](https://skillsmp.com/skills/wshobson-agents-plugins-api-scaffolding-skills-fastapi-templates-skill-md) | Python, FastAPI | fastapi, api, python backend |
| `angular-modern` | Angular Modern | [skillsmp.com](https://skillsmp.com/skills/jeffallan-claude-skills-skills-angular-architect-skill-md) | Angular 17+ | angular, typescript, frontend |
| `ui-ux-pro-max` | UI/UX Pro | [skillsmp.com](https://skillsmp.com/skills/nextlevelbuilder-ui-ux-pro-max-skill-claude-skills-ui-ux-pro-max-skill-md) | Design | ui, ux, design system |
| `openai-integration` | OpenAI API | [skillsmp.com](https://skillsmp.com/skills/openai-openai-agents-python-codex-skills-openai-knowledge-skill-md) | Python, OpenAI | openai, gpt, llm |

### External Skills (aitmpl.com)

| Skill ID | Name | Source URL | Tech Stack | Keywords |
|----------|------|------------|------------|----------|
| `code-review` | Code Reviewer | [aitmpl.com](https://www.aitmpl.com/component/skill/code-reviewer) | Any | review, pr, quality |
| `git-workflow` | Git Workflow | [aitmpl.com](https://www.aitmpl.com/plugin/git-workflow) | Git | git, commit, branch |
| `senior-data-engineer` | Data Engineering | [aitmpl.com](https://www.aitmpl.com/component/skill/senior-data-engineer) | Data, ETL | data, pipeline, etl |
| `react-tanstack` | React + TanStack | [aitmpl.com](https://www.aitmpl.com/component/skill/react-best-practices) | React, TanStack | react, query, router |
| `senior-prompt-engineer` | Prompt Engineering | [aitmpl.com](https://www.aitmpl.com/component/skill/senior-prompt-engineer) | AI/ML | prompt, llm, ai |

### Custom Skills (To Create)

| Skill ID | Name | Purpose | Projects Using |
|----------|------|---------|----------------|
| `scala-spring-patterns` | Scala + Spring | Spring Boot patterns for Scala | smile-app, DBricks_Optimizer, auth |
| `databricks-development` | Databricks Dev | Unity Catalog, Jobs, SDK | bp-informatica, DBricks_Optimizer |
| `bank-integration` | Bank Integration | ING/Revolut/Tink parsing | ing, tink |
| `oauth2-jwt` | OAuth2/JWT | Authentication patterns | smile-app |
| `product-sync` | Product Sync | API sync patterns | smile-price-manager |
| `informatica-xml` | Informatica XML | ETL XML parsing | bp-informatica |

---

## Agents Registry

### Global Agents (Workspace Level)

| Agent ID | Name | Skills | Triggers |
|----------|------|--------|----------|
| `code-reviewer` | Code Reviewer | code-review, git-workflow | pr_create, on_request |
| `doc-writer` | Documentation Writer | docx, pdf, pptx, xlsx | release, on_request |
| `devops` | DevOps Agent | git-workflow | infrastructure_change |
| `test-generator` | Test Generator | code-review, webapp-testing | feature_complete |
| `refactoring` | Refactoring Agent | code-review | tech_debt_sprint |

### Local Agents (Tech-Stack Specific)

| Agent ID | Name | Skills | Best For |
|----------|------|--------|----------|
| `database-agent` | Database Agent | database-implementation, postgresql, sqlserver, sql-review | Schema changes, migrations |
| `scala-backend` | Scala Backend | senior-data-engineer, scala-spring-patterns, flyway-migrations | Scala + Spring Boot |
| `frontend-agent` | Frontend Agent | frontend-design, ui-ux-pro-max, web-artifacts-builder | React, Angular, Vue |
| `python-backend` | Python Backend | fastapi, senior-data-engineer, python-dev | FastAPI, Flask, Django |
| `databricks-agent` | Databricks Agent | jupyter-notebook, python-dev, databricks-development | Notebooks, Unity Catalog |

### Project-Specific Agents

| Agent ID | Name | Skills | For Project Type |
|----------|------|--------|------------------|
| `sql-converter` | SQL Converter | oracle-sql, databricks-sql-converter, sql-review | Database migrations |
| `xml-parser` | XML Parser | informatica-xml | ETL migrations |
| `categorizer` | Categorizer Agent | openai-integration | ML classification |
| `api-integrator` | API Integration | product-sync | Third-party APIs |

---

## MCP Servers Registry

### Global MCP Servers (Always Available)

| Server ID | Name | Command | Purpose |
|-----------|------|---------|---------|
| `filesystem` | Filesystem | Built-in | File operations |
| `git` | Git | Built-in | Version control |
| `fetch` | HTTP Fetch | Built-in | API calls |
| `memory` | Memory | Built-in | Context persistence |

### Database MCP Servers

| Server ID | Name | Command | Env Vars |
|-----------|------|---------|----------|
| `postgres` | PostgreSQL | `npx -y @anthropic/mcp-postgres` | DATABASE_URL |
| `sqlserver` | SQL Server | `uvx mcp-sqlserver` | SQLSERVER_CONNECTION_STRING |
| `sqlite` | SQLite | `uvx mcp-sqlite --db-path ./data/db.sqlite` | - |
| `dbhub` | DbHub | `uvx dbhub` | - |

### Cloud MCP Servers

| Server ID | Name | Command | Env Vars |
|-----------|------|---------|----------|
| `databricks` | Databricks | `uvx mcp-databricks` | DATABRICKS_HOST, DATABRICKS_TOKEN |
| `azure` | Azure | `npx -y @anthropic/mcp-azure` | AZURE_SUBSCRIPTION_ID |
| `aws` | AWS | `npx -y @anthropic/mcp-aws` | AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY |

### Development MCP Servers

| Server ID | Name | Command | Env Vars |
|-----------|------|---------|----------|
| `jetbrains` | JetBrains IDE | `java -classpath ... McpStdioRunnerKt` | IJ_MCP_SERVER_PORT |
| `notion` | Notion | `npx -y @anthropic/mcp-notion` | NOTION_TOKEN |
| `github` | GitHub | `npx -y @anthropic/mcp-github` | GITHUB_TOKEN |

---

## Tech Stack → Tooling Mapping

Use this matrix to quickly identify relevant tools for a project:

### By Programming Language

| Language | Skills | Agents | MCP Servers |
|----------|--------|--------|-------------|
| **TypeScript/JavaScript** | react-tanstack, angular-modern, web-artifacts-builder | frontend-agent | - |
| **Python** | python-dev, fastapi, jupyter-notebook | python-backend, databricks-agent | - |
| **Scala** | scala-spring-patterns, senior-data-engineer | scala-backend | - |
| **SQL** | postgresql, sqlserver, sql-review, database-implementation | database-agent | postgres, sqlserver, sqlite |

### By Framework

| Framework | Skills | Agents |
|-----------|--------|--------|
| **React** | react-tanstack, web-artifacts-builder, ui-ux-pro-max | frontend-agent |
| **Angular** | angular-modern, ui-ux-pro-max | frontend-agent |
| **Spring Boot** | scala-spring-patterns, senior-data-engineer | scala-backend |
| **FastAPI** | fastapi, python-dev | python-backend |
| **Databricks** | databricks-development, jupyter-notebook | databricks-agent |

### By Project Type

| Project Type | Skills | Agents | MCP Servers |
|--------------|--------|--------|-------------|
| **Web App (Full-stack)** | frontend-design, database-implementation, git-workflow | frontend-agent, database-agent, code-reviewer | postgres/sqlite |
| **Mobile App** | frontend-design, ui-ux-pro-max | frontend-agent | - |
| **API Backend** | fastapi/scala-spring-patterns, database-implementation | python-backend/scala-backend, database-agent | postgres |
| **Data Pipeline** | senior-data-engineer, jupyter-notebook | databricks-agent, python-backend | databricks |
| **CLI Tool** | python-dev, git-workflow | python-backend, code-reviewer | - |

### By Feature Needs

| Feature | Skills | Agents | MCP Servers |
|---------|--------|--------|-------------|
| **Authentication** | oauth2-jwt | scala-backend/python-backend | - |
| **Database** | postgresql, database-implementation, flyway-migrations | database-agent | postgres, sqlserver |
| **Data Visualization** | xlsx, jupyter-notebook | databricks-agent | - |
| **AI/ML Integration** | openai-integration, senior-prompt-engineer | categorizer | - |
| **Third-party APIs** | product-sync | api-integrator | fetch |

---

## Querying the Registry

### Pseudo-code for Dynamic Lookup

```python
async def find_tools_for_project(project_classification: dict) -> ToolingRecommendation:
    """
    Query registry providers for matching tools.
    In production, this calls skillsmp.com, aitmpl.com APIs.
    """
    skills = []
    agents = []
    mcp_servers = []

    # Always include global tools
    skills.extend(CLAUDE_DEFAULT_SKILLS)
    agents.extend(GLOBAL_AGENTS)
    mcp_servers.extend(['filesystem', 'git', 'fetch'])

    # Match by language
    if project_classification['language'] in ['typescript', 'javascript']:
        skills.extend(['react-tanstack', 'web-artifacts-builder'])
        agents.append('frontend-agent')

    if project_classification['language'] == 'python':
        skills.extend(['python-dev', 'fastapi'])
        agents.append('python-backend')

    # Match by framework
    if 'react' in project_classification['frameworks']:
        skills.append('react-tanstack')

    if 'angular' in project_classification['frameworks']:
        skills.append('angular-modern')

    # Match by database
    if project_classification['database'] == 'postgresql':
        skills.extend(['postgresql', 'database-implementation'])
        mcp_servers.append('postgres')
        agents.append('database-agent')

    # Match by features
    if 'auth' in project_classification['features']:
        skills.append('oauth2-jwt')

    if 'data-visualization' in project_classification['features']:
        skills.extend(['xlsx', 'jupyter-notebook'])

    return ToolingRecommendation(
        skills=dedupe(skills),
        agents=dedupe(agents),
        mcp_servers=dedupe(mcp_servers)
    )
```

### Future: API Integration

When skillsmp.com provides an API:

```bash
# Search for skills
curl https://api.skillsmp.com/v1/skills/search?q=postgresql&stack=python

# Get skill details
curl https://api.skillsmp.com/v1/skills/postgresql

# Install skill
claude skill install skillsmp:postgresql
```
