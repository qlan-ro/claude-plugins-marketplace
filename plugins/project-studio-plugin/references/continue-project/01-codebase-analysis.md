# Phase 1: Codebase Analysis

## Objective
Deep analysis of an existing codebase to understand architecture, patterns, and current state before adding new features.

## Entry Criteria
- User has pointed to an existing project directory
- Project has some code already (not empty)

## Why This Phase Matters
Before adding features to an existing project, we need to understand:
- What technology choices were made
- What patterns are established
- What already exists (to avoid rebuilding)
- What conventions to follow

This prevents new code from conflicting with existing patterns.

---

## Key Activities

### 1. Project Structure Discovery

Analyze the directory structure:

```bash
# Find key directories
find . -type d -name "src" -o -name "app" -o -name "lib" -o -name "components"

# Find config files
ls -la *.json *.yaml *.toml *.config.* 2>/dev/null

# Find package manifests
ls package.json requirements.txt Cargo.toml build.sbt pom.xml go.mod 2>/dev/null
```

**Output:**
```yaml
structure:
  root: /path/to/project
  source_dirs: [src/, app/, lib/]
  test_dirs: [tests/, __tests__/, spec/]
  config_files: [package.json, tsconfig.json, ...]
  has_monorepo: true/false
```

### 2. Tech Stack Detection

**Package Analysis:**
```bash
# Node.js
cat package.json | jq '.dependencies, .devDependencies'

# Python
cat requirements.txt pyproject.toml

# JVM
cat build.sbt pom.xml build.gradle
```

**Infer from files:**
| Files Found | Technology |
|-------------|------------|
| `package.json` + `tsconfig.json` | TypeScript/Node |
| `next.config.js` | Next.js |
| `vite.config.ts` | Vite |
| `angular.json` | Angular |
| `requirements.txt` + `manage.py` | Django |
| `requirements.txt` + `main.py` | FastAPI/Flask |
| `build.sbt` | Scala/sbt |
| `pom.xml` | Java/Maven |
| `go.mod` | Go |
| `Cargo.toml` | Rust |

**Output:**
```yaml
tech_stack:
  languages: [typescript, python]
  frontend:
    framework: react
    version: "18.2"
    ui_library: tailwind
    state_management: zustand
  backend:
    framework: fastapi
    version: "0.100"
  database:
    type: postgresql
    orm: prisma
  build_tools: [vite, docker]
  testing: [vitest, pytest]
```

### 3. Data Model Extraction

**Find schema definitions:**
```bash
# Prisma
cat prisma/schema.prisma

# SQLAlchemy
grep -r "class.*Base" --include="*.py"

# TypeORM
grep -r "@Entity" --include="*.ts"

# Raw SQL migrations
ls db/migrations/ migrations/ alembic/versions/
```

**Output:**
```yaml
data_model:
  orm: prisma
  entities:
    - name: User
      fields: [id, email, name, createdAt]
      relations: [posts, comments]
    - name: Post
      fields: [id, title, content, authorId, createdAt]
      relations: [author, comments]
  migrations_dir: prisma/migrations/
  migration_count: 12
```

### 4. API Surface Discovery

**Find endpoints:**
```bash
# FastAPI
grep -r "@app\.\(get\|post\|put\|delete\)" --include="*.py"
grep -r "@router\.\(get\|post\|put\|delete\)" --include="*.py"

# Express
grep -r "app\.\(get\|post\|put\|delete\)" --include="*.ts" --include="*.js"
grep -r "router\.\(get\|post\|put\|delete\)" --include="*.ts" --include="*.js"

# Next.js API routes
ls -la app/api/**/route.ts pages/api/**/*.ts 2>/dev/null
```

**Output:**
```yaml
api:
  style: REST
  base_path: /api/v1
  endpoints:
    - method: GET
      path: /users
      handler: get_users
      file: src/routes/users.py
    - method: POST
      path: /users
      handler: create_user
      file: src/routes/users.py
    # ...
  auth_pattern: JWT Bearer token
  middleware: [cors, auth, logging]
```

### 5. Component Inventory (Frontend)

**Find components:**
```bash
# React components
find src/components -name "*.tsx" -o -name "*.jsx" | head -50

# Vue components
find src/components -name "*.vue" | head -50

# Angular components
find src/app -name "*.component.ts" | head -50
```

**Analyze patterns:**
```bash
# Check for common patterns
grep -r "useState\|useEffect\|useQuery" --include="*.tsx" | head -20
grep -r "createContext\|useContext" --include="*.tsx" | head -10
```

**Output:**
```yaml
frontend:
  component_dir: src/components/
  components:
    - name: Button
      path: src/components/ui/Button.tsx
      type: ui-primitive
    - name: UserCard
      path: src/components/users/UserCard.tsx
      type: feature
    - name: Dashboard
      path: src/components/pages/Dashboard.tsx
      type: page
  patterns:
    state: [useState, useQuery (TanStack)]
    styling: tailwind classes
    forms: react-hook-form
  design_system: shadcn/ui
```

### 6. Existing Feature Detection

**Infer features from code:**

| Code Pattern | Likely Feature |
|--------------|----------------|
| `login`, `auth`, `session` | Authentication |
| `signup`, `register` | User Registration |
| `profile`, `settings` | User Profile |
| `dashboard` | Dashboard |
| `upload`, `file`, `attachment` | File Upload |
| `search`, `filter`, `query` | Search/Filter |
| `notification`, `alert` | Notifications |
| `payment`, `stripe`, `checkout` | Payments |
| `admin`, `manage` | Admin Panel |

**Output:**
```yaml
existing_features:
  - name: User Authentication
    status: complete
    evidence: [src/auth/, login page, JWT middleware]
  - name: User Profile
    status: complete
    evidence: [profile page, settings API]
  - name: Dashboard
    status: partial
    evidence: [dashboard page exists, missing charts]
  - name: Search
    status: not_started
    evidence: [no search components found]
```

### 7. Convention Detection

**Code style:**
```bash
# Check for linters/formatters
cat .eslintrc* .prettierrc* biome.json ruff.toml 2>/dev/null

# Check naming patterns
ls src/components/ | head -10  # PascalCase? kebab-case?

# Check test patterns
ls tests/ __tests__/ | head -10
```

**Output:**
```yaml
conventions:
  naming:
    components: PascalCase
    files: kebab-case
    functions: camelCase
    constants: UPPER_SNAKE_CASE
  formatting:
    tool: prettier
    config: .prettierrc
  linting:
    tool: eslint
    config: .eslintrc.js
  testing:
    framework: vitest
    pattern: "*.test.ts"
    location: alongside  # or "tests/"
  git:
    branch_pattern: feature/*
    commit_style: conventional
```

---

## Output Artifact

Create `docs/CODEBASE_ANALYSIS.md`:

```markdown
# Codebase Analysis: {PROJECT_NAME}

**Analyzed:** {DATE}
**Root:** {PATH}

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | React + TypeScript | 18.2 |
| UI | Tailwind + shadcn/ui | 3.4 |
| Backend | FastAPI | 0.100 |
| Database | PostgreSQL + Prisma | 15 |
| Testing | Vitest + Pytest | - |

## Data Model

{Entity diagram or list}

## API Surface

| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/users | List users |
| POST | /api/users | Create user |
| ... | ... | ... |

## Existing Features

| Feature | Status | Evidence |
|---------|--------|----------|
| Authentication | ✅ Complete | auth/, JWT middleware |
| User Profile | ✅ Complete | profile page |
| Dashboard | 🟡 Partial | page exists, no charts |
| Search | ❌ Not Started | - |

## Conventions

- Components: PascalCase in `src/components/`
- Tests: `*.test.ts` alongside source
- Commits: Conventional commits
- Branches: `feature/*`, `fix/*`

## Key Files

| Purpose | Path |
|---------|------|
| Entry point | src/main.tsx |
| Routes | src/routes/ |
| API client | src/lib/api.ts |
| DB schema | prisma/schema.prisma |
| Types | src/types/ |
```

---

## Phase Gate Checklist

Before proceeding to Infer Product PRD:
- [ ] Project structure mapped
- [ ] Tech stack identified
- [ ] Data model extracted
- [ ] API endpoints catalogued
- [ ] Existing features detected
- [ ] Conventions documented
- [ ] `docs/CODEBASE_ANALYSIS.md` created
- [ ] User has reviewed and confirmed analysis accuracy
