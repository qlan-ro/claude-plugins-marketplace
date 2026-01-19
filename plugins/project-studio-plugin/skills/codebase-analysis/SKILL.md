---
name: codebase-analysis
description: |
  Deep codebase analysis for understanding existing projects. Use this skill when:
  - Analyzing an unfamiliar codebase
  - Detecting tech stack and patterns
  - Extracting data models and API surface
  - Documenting existing conventions

  This skill is domain-specific - it knows HOW to analyze code, not workflow phases.
---

# Codebase Analysis

Systematically analyze existing codebases to extract implicit knowledge.

## Analysis Process

### Step 1: Project Structure Discovery

```bash
# Key commands
ls -la                              # Root overview
find . -type f -name "*.json" | head -20   # Config files
find . -type d -maxdepth 2                 # Directory structure
```

Identify:
- Project root markers (package.json, Cargo.toml, go.mod)
- Source directories (src/, app/, lib/)
- Test directories (tests/, __tests__, spec/)
- Config files (tsconfig.json, .env.example)

### Step 2: Tech Stack Detection

| File/Pattern | Indicates |
|--------------|-----------|
| package.json | Node.js |
| next.config.js | Next.js |
| vite.config.ts | Vite |
| tsconfig.json | TypeScript |
| tailwind.config.js | Tailwind CSS |
| prisma/schema.prisma | Prisma ORM |
| drizzle.config.ts | Drizzle ORM |
| docker-compose.yml | Docker |
| Cargo.toml | Rust |
| go.mod | Go |
| pyproject.toml | Python |

### Step 3: Data Model Extraction

Look for:
1. **Database schemas** - Prisma, Drizzle, TypeORM, SQLAlchemy
2. **Type definitions** - TypeScript interfaces, Go structs, Pydantic models
3. **API contracts** - OpenAPI specs, tRPC routers, GraphQL schemas
4. **Validation schemas** - Zod, Yup, Joi definitions

Extract entity structure:
```
Entity: User
Fields: id (UUID), email (string, unique), name (string), createdAt (datetime)
Relationships: has many Posts, has one Profile
```

### Step 4: API Surface Discovery

```bash
# Next.js API routes
find . -path "*/api/*" -name "*.ts"

# Express/Fastify routes
grep -r "app.get\|app.post\|router\." --include="*.ts"

# tRPC routers
grep -r "router\|procedure" --include="*.ts" | head -30
```

Document as:
| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | /api/users | List users | Yes |
| POST | /api/users | Create user | Yes |

### Step 5: Component Inventory

For frontend projects:
```bash
# React/Vue/Svelte components
find . -path "*/components/*" -name "*.tsx"

# Page components
find . -path "*/app/*" -name "page.tsx"
find . -path "*/pages/*" -name "*.tsx"
```

Categorize:
- **UI Components** - Buttons, inputs, cards (generic)
- **Feature Components** - Domain-specific (UserCard, PostList)
- **Layout Components** - Shells, wrappers, containers
- **Page Components** - Route-level views

### Step 6: Existing Feature Detection

Identify implemented functionality:
- Authentication (login, signup, logout, password reset)
- CRUD operations per entity
- Dashboard/admin features
- User settings/profile
- Integrations (payments, email, analytics)

Mark each as:
- **Complete** - Full functionality working
- **Partial** - Some parts implemented
- **Stub** - Placeholder only

### Step 7: Convention Detection

**Naming Conventions**
- File naming: kebab-case, camelCase, PascalCase
- Function naming: verbs (getUser), nouns (userService)
- Component naming: PascalCase with suffix (UserCard)

**Code Patterns**
- State management: useState, Context, Redux, Zustand, Pinia
- Data fetching: fetch, axios, React Query, SWR, tRPC
- Error handling: try/catch, Result types, error boundaries
- Logging: console, pino, winston

**Folder Structure**
- Feature-based: /features/{name}/
- Type-based: /components/, /hooks/, /utils/
- Hybrid: Both patterns

## Output Template

Create `docs/CODEBASE_ANALYSIS.md`:

```markdown
# Codebase Analysis Report

## Project Overview
- **Name:** {from package.json or directory}
- **Type:** {Web app, API, CLI, Library}
- **Language:** {TypeScript, JavaScript, Python, etc.}
- **Last Updated:** {from git or file dates}

## Tech Stack

### Frontend
| Technology | Version | Usage |
|------------|---------|-------|
| {Framework} | {X.x} | {Purpose} |

### Backend
| Technology | Version | Usage |
|------------|---------|-------|
| {Runtime} | {X.x} | {Purpose} |

### Database
| Technology | Version | Usage |
|------------|---------|-------|
| {DB} | {X.x} | {Purpose} |

## Data Model

### Entities
| Entity | Key Fields | Relationships |
|--------|------------|---------------|
| User | id, email, name | has many Posts |

### Schema Location
{Path to schema files}

## API Surface

### Endpoints
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | /api/users | Yes | List users |

## Components

### UI Components ({count})
{List of generic components}

### Feature Components ({count})
{List of domain components}

### Pages ({count})
{List of pages/routes}

## Existing Features

### Complete
- [x] {Feature} - {location}

### Partial
- [ ] {Feature} - {what's missing}

### Stub/Placeholder
- [ ] {Feature} - {not implemented}

## Conventions

### Naming
- Files: {pattern}
- Functions: {pattern}
- Components: {pattern}

### Patterns
- State: {approach}
- Fetching: {approach}
- Errors: {approach}

### Structure
```
{folder tree}
```

## Tech Debt & Issues
| Issue | Severity | Location |
|-------|----------|----------|
| {Description} | High/Med/Low | {path} |

## Recommendations
1. {Recommendation}
2. {Recommendation}
```

## Analysis Mindset

1. **Be thorough** - Check multiple patterns, don't assume
2. **Document what IS, not what SHOULD BE** - No redesigning
3. **Note inconsistencies** - Projects have legacy patterns
4. **Extract implicit knowledge** - Make it explicit
5. **Respect existing choices** - They may have good reasons
