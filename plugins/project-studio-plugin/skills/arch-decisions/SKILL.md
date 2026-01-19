---
name: arch-decisions
description: |
  Software architecture decisions and technical design. Use this skill when:
  - Selecting technology stacks
  - Designing data models
  - Defining API structure
  - Making security and scalability decisions

  This skill is domain-specific - it knows HOW to architect, not workflow phases.
---

# Architecture Decisions

Make informed technology decisions with clear trade-offs.

## Decision-Making Style

For every major decision, present options with pros/cons:

```markdown
### Decision: Frontend Framework

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Next.js** | SSR, great DX, Vercel deploy | React lock-in | SEO-important apps |
| **Remix** | Full-stack, progressive enhancement | Smaller ecosystem | Form-heavy apps |
| **SvelteKit** | Performance, smaller bundle | Smaller talent pool | Performance-critical |

**Recommendation:** Next.js - best balance for this use case because {reason}.
```

Always explain WHY you recommend something.

## Architecture Document Sections

### 1. Technology Stack

```markdown
## Technology Stack

### Frontend
- **Framework:** {Choice} - {One-line rationale}
- **Styling:** {Choice} - {One-line rationale}
- **State Management:** {Choice} - {One-line rationale}

### Backend
- **Runtime:** {Choice} - {One-line rationale}
- **Framework:** {Choice} - {One-line rationale}
- **API Style:** REST / GraphQL / tRPC - {One-line rationale}

### Database
- **Primary:** {Choice} - {One-line rationale}
- **ORM:** {Choice} - {One-line rationale}
- **Caching:** {Choice if applicable}

### Infrastructure
- **Hosting:** {Choice} - {One-line rationale}
- **CI/CD:** {Choice}
- **Monitoring:** {Choice}
```

### 2. Data Model

```markdown
## Data Model

### Core Entities

#### User
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | String | Unique, Required | Login email |
| name | String | Required | Display name |
| createdAt | DateTime | Default: now | Account creation |

### Relationships
- User has many Posts (1:N)
- Post belongs to User (N:1)
- User has many Tags through PostTags (M:N)

### Entity Diagram
```
[User] 1──N [Post] N──M [Tag]
         └── N [Comment]
```
```

### 3. API Design

```markdown
## API Design

### Style: {REST / GraphQL / tRPC}

### Authentication Endpoints
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/auth/signup | Create account | None |
| POST | /api/auth/login | Authenticate | None |
| POST | /api/auth/logout | End session | Required |

### Resource: {Entity}
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/{resource} | List all | Required |
| GET | /api/{resource}/:id | Get one | Required |
| POST | /api/{resource} | Create | Required |
| PUT | /api/{resource}/:id | Update | Required |
| DELETE | /api/{resource}/:id | Delete | Required |

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "field": "email"
  }
}
```
```

### 4. Security Architecture

```markdown
## Security

### Authentication
- **Method:** {JWT / Session / OAuth}
- **Token Storage:** {httpOnly cookies / Authorization header}
- **Session Duration:** {Duration}
- **Refresh Strategy:** {If applicable}

### Authorization
- **Model:** {RBAC / ABAC / Simple}
- **Roles:** Admin, User, Guest
- **Permission Check:** {Middleware / Per-route}

### Data Protection
- **Passwords:** bcrypt with cost factor 12
- **Sensitive Data:** Encrypted at rest
- **Transport:** TLS 1.3

### Security Headers
- Content-Security-Policy
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
```

### 5. Project Structure

```markdown
## Project Structure

```
{project}/
├── src/
│   ├── app/              # Next.js app router
│   │   ├── api/          # API routes
│   │   ├── (auth)/       # Auth pages (grouped)
│   │   └── (dashboard)/  # Protected pages (grouped)
│   ├── components/
│   │   ├── ui/           # Generic UI components
│   │   └── features/     # Domain-specific components
│   ├── lib/
│   │   ├── db.ts         # Database client
│   │   ├── auth.ts       # Auth utilities
│   │   └── api.ts        # API helpers
│   └── types/            # TypeScript types
├── prisma/
│   └── schema.prisma     # Database schema
├── public/               # Static assets
└── tests/                # Test files
```
```

## Stack Recommendations by Project Type

### SaaS Application
- Next.js + TypeScript + Tailwind
- PostgreSQL + Prisma
- NextAuth or Clerk for auth
- Vercel or Railway hosting

### Internal Tool
- Next.js or Remix
- PostgreSQL or SQLite
- Simple session auth
- Docker self-host or Fly.io

### API-First Service
- Node.js + Fastify or Hono
- PostgreSQL + Drizzle
- JWT authentication
- AWS Lambda or Cloudflare Workers

### Mobile App Backend
- Node.js + Express or NestJS
- PostgreSQL + Prisma
- JWT + refresh tokens
- AWS or GCP

## Continue-Project Mode (Documentation)

When documenting an EXISTING codebase:

1. **Document what IS, not what SHOULD BE**
2. **Note tech debt** but don't redesign
3. **Capture implicit conventions**
4. **Identify extension points** for new features

Add a Tech Debt section:
```markdown
## Tech Debt
| Issue | Severity | Recommendation |
|-------|----------|----------------|
| No input validation | High | Add Zod schemas |
| Mixed async patterns | Medium | Standardize on async/await |
```

## Output Template

Create `docs/ARCHITECTURE.md` with the sections above.

## Decision Checklist

Before finalizing, ensure:
- [ ] Every choice has a stated rationale
- [ ] Trade-offs are acknowledged
- [ ] Data model covers all PRD features
- [ ] API endpoints support required operations
- [ ] Security approach is defined
- [ ] File structure is clear

## Add-Feature Mode (Amendment)

When adding features via `/add-feature` that require architecture changes:

### Rules for Amendment Mode

1. **DO NOT redesign** existing architecture
2. **READ** existing ARCHITECTURE.md first
3. **PRESERVE** all existing decisions and rationale
4. **ADD** new sections for new capabilities
5. **UPDATE** affected sections minimally
6. **DOCUMENT** breaking changes if any

### Process

1. **Identify what's needed:**
   - New data models?
   - New API endpoints?
   - New integrations?
   - Schema migrations?

2. **Add new sections:**
```markdown
## Amendments (Added {date})

### New Feature: {Feature Name}

#### Data Model Additions
| Entity | Fields | Relationship |
|--------|--------|--------------|
| ThemePreference | userId, theme, updatedAt | User 1:1 |

#### New API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/user/theme | Get preference |
| PUT | /api/user/theme | Update preference |

#### Migration Required
- Add `theme_preference` table
- Add `theme` column to user_settings (if exists)
```

3. **Note impacts on existing:**
```markdown
#### Impacts on Existing
- **User entity:** No changes needed
- **Auth flow:** No changes needed
- **API structure:** New endpoint group added
```

### Output

Updated `docs/ARCHITECTURE.md` with:
- New sections for additional capabilities
- Existing content UNCHANGED (unless directly affected)
- Clear separation of amendments from original
