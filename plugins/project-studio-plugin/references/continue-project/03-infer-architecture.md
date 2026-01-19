# Phase 3: Infer Architecture

## Objective
Document the existing architecture by analyzing the codebase. This is documentation, not redesign.

## Entry Criteria
- Codebase Analysis complete
- Product PRD complete with new features identified

## Why This Phase Matters
New features must follow existing architecture patterns. Documenting what exists:
- Prevents conflicting patterns in new code
- Gives Feature PRDs concrete references (field names, API patterns)
- Reduces hallucination by grounding in actual code

---

## Key Activities

### 1. Document Tech Stack Decisions

From codebase analysis, document **why** these choices work (not proposing alternatives):

```markdown
## Technology Stack

### Frontend
| Technology | Version | Usage |
|------------|---------|-------|
| React | 18.2 | UI framework |
| TypeScript | 5.0 | Type safety |
| Tailwind | 3.4 | Styling |
| TanStack Query | 5.0 | Data fetching |
| Zustand | 4.0 | Client state |

**Patterns to follow:**
- Components in `src/components/` using PascalCase
- Hooks in `src/hooks/` prefixed with `use`
- API calls via `src/lib/api.ts` client

### Backend
| Technology | Version | Usage |
|------------|---------|-------|
| FastAPI | 0.100 | API framework |
| SQLAlchemy | 2.0 | ORM |
| PostgreSQL | 15 | Database |
| Alembic | 1.12 | Migrations |

**Patterns to follow:**
- Routes in `src/routes/` grouped by resource
- Models in `src/models/`
- Schemas (Pydantic) in `src/schemas/`
```

### 2. Document Data Model

Extract and document the actual schema:

```markdown
## Data Model

### Entity: User
**Table:** `users`
**File:** `src/models/user.py` or `prisma/schema.prisma`

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK |
| email | String | Unique, Not Null |
| name | String | Not Null |
| password_hash | String | Not Null |
| created_at | DateTime | Default: now() |
| updated_at | DateTime | Auto-update |

**Relations:**
- Has many: Post, Comment

### Entity: Post
**Table:** `posts`

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK |
| title | String | Not Null |
| content | Text | Not Null |
| author_id | UUID | FK → users.id |
| created_at | DateTime | Default: now() |

**Relations:**
- Belongs to: User (author)
- Has many: Comment
```

Include an ERD if complex:
```
┌──────────┐       ┌──────────┐       ┌──────────┐
│   User   │───┬───│   Post   │───────│ Comment  │
└──────────┘   │   └──────────┘       └──────────┘
               │
               └───────────────────────────────────┘
```

### 3. Document API Patterns

From actual endpoints:

```markdown
## API Design

### Base URL
`/api/v1`

### Authentication
- Method: JWT Bearer token
- Header: `Authorization: Bearer <token>`
- Middleware: `src/middleware/auth.py`

### Endpoint Patterns

| Method | Path Pattern | Example | Handler Location |
|--------|--------------|---------|------------------|
| GET | /{resource} | /users | List all |
| GET | /{resource}/{id} | /users/123 | Get one |
| POST | /{resource} | /users | Create |
| PUT | /{resource}/{id} | /users/123 | Update |
| DELETE | /{resource}/{id} | /users/123 | Delete |

### Response Format
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  }
}
```

### Error Format
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

### Existing Endpoints

| Method | Path | Purpose | File |
|--------|------|---------|------|
| POST | /auth/login | Login | routes/auth.py |
| POST | /auth/register | Register | routes/auth.py |
| GET | /users/me | Current user | routes/users.py |
| PUT | /users/me | Update profile | routes/users.py |
| GET | /posts | List posts | routes/posts.py |
| POST | /posts | Create post | routes/posts.py |
```

### 4. Document Component Patterns

From actual components:

```markdown
## Component Architecture

### Directory Structure
```
src/components/
├── ui/           # Primitives (Button, Input, Card)
├── forms/        # Form components
├── layout/       # Layout (Header, Sidebar, Footer)
├── features/     # Feature-specific (UserCard, PostList)
└── pages/        # Page components
```

### Component Conventions

**UI Components:**
- Location: `src/components/ui/`
- Style: Tailwind classes
- Props: TypeScript interfaces in same file
- Example: `Button.tsx`

**Feature Components:**
- Location: `src/components/features/`
- Data: Use TanStack Query hooks
- Example: `UserCard.tsx`

**Page Components:**
- Location: `src/components/pages/` or `app/`
- Routing: React Router / Next.js
- Example: `Dashboard.tsx`

### Existing Components

| Component | Path | Purpose |
|-----------|------|---------|
| Button | ui/Button.tsx | Primary UI button |
| Card | ui/Card.tsx | Content container |
| Input | ui/Input.tsx | Form input |
| UserCard | features/UserCard.tsx | User display |
| PostList | features/PostList.tsx | Post listing |
| Dashboard | pages/Dashboard.tsx | Main dashboard |
```

### 5. Document State Management

```markdown
## State Management

### Server State
- Tool: TanStack Query
- Cache: 5 minute stale time
- Pattern: Custom hooks in `src/hooks/`

**Example:**
```typescript
// src/hooks/useUsers.ts
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.get('/users')
  })
}
```

### Client State
- Tool: Zustand
- Stores: `src/stores/`

**Existing Stores:**
| Store | File | Purpose |
|-------|------|---------|
| authStore | stores/auth.ts | User session |
| uiStore | stores/ui.ts | UI state (modals, sidebar) |
```

### 6. Document Security Patterns

```markdown
## Security

### Authentication
- Method: JWT
- Storage: httpOnly cookie / localStorage
- Refresh: {pattern used}

### Authorization
- Pattern: Role-based (admin, user)
- Implementation: Middleware checks
- Location: `src/middleware/auth.py`

### Input Validation
- Frontend: Zod / react-hook-form
- Backend: Pydantic schemas
```

---

## Output Artifact

Create `docs/ARCHITECTURE.md`:

```markdown
# Architecture: {PROJECT_NAME}

**Inferred from codebase:** {DATE}
**Status:** Documentation of existing architecture

---

## Tech Stack

{From Section 1}

---

## Data Model

{From Section 2}

---

## API Design

{From Section 3}

---

## Component Architecture

{From Section 4}

---

## State Management

{From Section 5}

---

## Security

{From Section 6}

---

## Conventions for New Code

When adding new features, follow these patterns:

### Adding a New Entity
1. Create model in `src/models/{name}.py`
2. Create schema in `src/schemas/{name}.py`
3. Create migration: `alembic revision --autogenerate`
4. Create routes in `src/routes/{name}.py`

### Adding a New Component
1. Create in appropriate directory (`ui/`, `features/`, `pages/`)
2. Use existing design tokens (colors, spacing)
3. Follow TypeScript patterns from existing components

### Adding a New API Endpoint
1. Add route in `src/routes/{resource}.py`
2. Follow existing response format
3. Add auth middleware if needed
4. Document in this file
```

---

## Phase Gate Checklist

Before proceeding to Infer Design:
- [ ] Tech stack documented
- [ ] Data model extracted with all fields
- [ ] API patterns documented
- [ ] Component patterns documented
- [ ] State management documented
- [ ] Security patterns documented
- [ ] `docs/ARCHITECTURE.md` created
- [ ] User has confirmed architecture accuracy
