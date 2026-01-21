# Scaffolding Feature PRD Template

This template generates the Project Scaffolding feature PRD based on the tech stack from Architecture.

## Usage

Copy and customize this template for the specific tech stack. The scaffolding feature MUST be Feature #1.

---

## Template: TypeScript/Node.js (Vite + React)

```markdown
# PRD: Project Scaffolding

## Introduction
Initialize the project with TypeScript, build tooling, testing framework, and development infrastructure. This foundation enables all subsequent features to be built, tested, and verified.

## Goals
- Working development environment with hot reload
- Type checking for code quality
- Test runner for verification
- Linting for consistency
- Build scripts for deployment

## User Stories

### US-001: Initialize package.json and dependencies
**Description:** As a developer, I need a package.json with core dependencies so I can install and manage packages.

**Acceptance Criteria:**
- [ ] package.json exists with project name and version
- [ ] Dependencies: react, react-dom
- [ ] Dev dependencies: typescript, vite, @types/react, @types/react-dom
- [ ] Scripts: dev, build, preview
- [ ] `npm install` completes without errors

### US-002: Configure TypeScript
**Description:** As a developer, I need TypeScript configuration for type safety.

**Acceptance Criteria:**
- [ ] tsconfig.json exists with strict mode enabled
- [ ] Include src/**/*
- [ ] JSX support configured for React
- [ ] `npx tsc --noEmit` passes (typecheck)

### US-003: Configure Vite
**Description:** As a developer, I need Vite configured for development and builds.

**Acceptance Criteria:**
- [ ] vite.config.ts exists
- [ ] React plugin configured
- [ ] `npm run dev` starts dev server
- [ ] `npm run build` produces dist/ folder

### US-004: Create project structure
**Description:** As a developer, I need the basic folder structure in place.

**Acceptance Criteria:**
- [ ] src/ directory exists
- [ ] src/main.tsx as entry point
- [ ] src/App.tsx with minimal component
- [ ] index.html references main.tsx
- [ ] App renders "Hello World" in browser

### US-005: Configure testing (Vitest)
**Description:** As a developer, I need a test runner to verify code works.

**Acceptance Criteria:**
- [ ] vitest and @testing-library/react installed
- [ ] vitest.config.ts configured
- [ ] test script in package.json
- [ ] src/App.test.tsx with basic render test
- [ ] `npm test` runs and passes

### US-006: Configure linting and formatting
**Description:** As a developer, I need consistent code style enforcement.

**Acceptance Criteria:**
- [ ] eslint installed with TypeScript + React rules
- [ ] .eslintrc.cjs configured
- [ ] prettier installed
- [ ] .prettierrc configured
- [ ] lint script in package.json
- [ ] `npm run lint` passes

## Non-Goals
- No CI/CD pipeline (add in later feature if needed)
- No deployment configuration
- No environment variables setup beyond basics

## Technical Considerations
- Use ESM modules throughout
- Keep bundle size minimal for MVP
- Prefer Vitest over Jest for Vite compatibility
```

---

## Template: TypeScript/Node.js (Next.js)

```markdown
# PRD: Project Scaffolding

## Introduction
Initialize Next.js project with TypeScript, testing, and linting. This foundation enables all subsequent features.

## Goals
- Working Next.js development environment
- Type checking for code quality
- Test runner for verification
- Linting for consistency

## User Stories

### US-001: Initialize Next.js project
**Description:** As a developer, I need a Next.js project with TypeScript.

**Acceptance Criteria:**
- [ ] package.json exists with next, react, react-dom
- [ ] TypeScript and @types/* packages installed
- [ ] next.config.js configured
- [ ] `npm run dev` starts on localhost:3000

### US-002: Configure TypeScript
**Description:** As a developer, I need strict TypeScript configuration.

**Acceptance Criteria:**
- [ ] tsconfig.json with strict mode
- [ ] Next.js paths configured
- [ ] `npm run typecheck` (or tsc --noEmit) passes

### US-003: Create App Router structure
**Description:** As a developer, I need the basic Next.js App Router structure.

**Acceptance Criteria:**
- [ ] src/app/ directory exists
- [ ] src/app/layout.tsx with RootLayout
- [ ] src/app/page.tsx with home page
- [ ] Renders "Hello World" at localhost:3000

### US-004: Configure testing (Vitest or Jest)
**Description:** As a developer, I need a test runner.

**Acceptance Criteria:**
- [ ] Test framework installed and configured
- [ ] test script in package.json
- [ ] src/app/page.test.tsx with basic test
- [ ] `npm test` runs and passes

### US-005: Configure ESLint
**Description:** As a developer, I need linting configured.

**Acceptance Criteria:**
- [ ] ESLint configured via next lint
- [ ] lint script in package.json
- [ ] `npm run lint` passes

## Non-Goals
- No database setup (separate feature)
- No authentication (separate feature)
- No deployment configuration

## Technical Considerations
- Use App Router (not Pages Router)
- Server Components by default
- Keep initial bundle minimal
```

---

## Template: Electron + TypeScript

```markdown
# PRD: Project Scaffolding

## Introduction
Initialize Electron project with TypeScript for main and renderer processes.

## Goals
- Working Electron development environment
- Type checking for both processes
- Build tooling for packaging
- Test runner for verification

## User Stories

### US-001: Initialize package.json and dependencies
**Description:** As a developer, I need core Electron dependencies.

**Acceptance Criteria:**
- [ ] package.json with electron as dev dependency
- [ ] Scripts: dev, build, package
- [ ] `npm install` completes without errors

### US-002: Configure TypeScript
**Description:** As a developer, I need TypeScript for both processes.

**Acceptance Criteria:**
- [ ] tsconfig.json for main process
- [ ] tsconfig.web.json for renderer (if separate)
- [ ] Strict mode enabled
- [ ] `npm run typecheck` passes

### US-003: Create main process entry
**Description:** As a developer, I need the main process configured.

**Acceptance Criteria:**
- [ ] src/main/index.ts exists
- [ ] Creates BrowserWindow
- [ ] Loads renderer HTML or URL
- [ ] `npm run dev` opens Electron window

### US-004: Create renderer process
**Description:** As a developer, I need the renderer process configured.

**Acceptance Criteria:**
- [ ] src/renderer/ directory exists
- [ ] index.html with root div
- [ ] main.tsx entry point
- [ ] Basic React/Svelte/Vue component renders

### US-005: Configure build tooling
**Description:** As a developer, I need build tooling for packaging.

**Acceptance Criteria:**
- [ ] electron-builder or electron-forge configured
- [ ] `npm run build` produces distributable

### US-006: Configure testing
**Description:** As a developer, I need testing configured.

**Acceptance Criteria:**
- [ ] Test framework installed
- [ ] Basic unit test passes
- [ ] `npm test` runs successfully

## Non-Goals
- No auto-update mechanism
- No code signing
- No multi-platform build (start with current OS)

## Technical Considerations
- Separate main and renderer TypeScript configs
- Use contextBridge for IPC security
- Keep renderer as simple web app initially
```

---

## Template: Python

```markdown
# PRD: Project Scaffolding

## Introduction
Initialize Python project with type hints, testing, and linting.

## Goals
- Working Python development environment
- Type checking with mypy
- Test runner (pytest)
- Linting (ruff)

## User Stories

### US-001: Initialize pyproject.toml
**Description:** As a developer, I need project configuration.

**Acceptance Criteria:**
- [ ] pyproject.toml exists with project metadata
- [ ] Python version specified (>=3.11)
- [ ] Dependencies section defined
- [ ] `pip install -e .` works

### US-002: Create project structure
**Description:** As a developer, I need the basic folder structure.

**Acceptance Criteria:**
- [ ] src/{package_name}/ directory
- [ ] src/{package_name}/__init__.py
- [ ] src/{package_name}/main.py with entry point
- [ ] tests/ directory

### US-003: Configure type checking
**Description:** As a developer, I need type checking configured.

**Acceptance Criteria:**
- [ ] mypy installed as dev dependency
- [ ] mypy.ini or pyproject.toml [tool.mypy] configured
- [ ] `mypy src/` passes

### US-004: Configure testing
**Description:** As a developer, I need pytest configured.

**Acceptance Criteria:**
- [ ] pytest installed as dev dependency
- [ ] tests/test_main.py with basic test
- [ ] `pytest` runs and passes

### US-005: Configure linting
**Description:** As a developer, I need linting configured.

**Acceptance Criteria:**
- [ ] ruff installed as dev dependency
- [ ] ruff configuration in pyproject.toml
- [ ] `ruff check .` passes

## Non-Goals
- No Docker configuration
- No CI/CD pipeline
- No virtual environment automation

## Technical Considerations
- Use src/ layout
- Type hints on all functions
- Follow PEP 8 style
```

---

## How to Use This Template

1. **Identify tech stack** from Architecture document
2. **Copy appropriate template** above
3. **Customize** based on specific needs:
   - Add/remove stories based on actual stack
   - Adjust acceptance criteria for project specifics
   - Add framework-specific configuration
4. **Save as** `docs/features/01-project-scaffolding/PRD.md`

## Key Principles

1. **Minimal but complete** - Just enough to run dev, build, test, lint
2. **Verifiable criteria** - Every criterion can be checked by running a command
3. **No business logic** - Scaffolding is pure infrastructure
4. **Independence** - Should work before any other features exist
