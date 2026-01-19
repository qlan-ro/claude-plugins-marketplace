# Phase 5: Development

## Objective
Build the application following the implementation plan with high-quality, tested code.

## Entry Criteria
- Approved Implementation Plan from Phase 4
- Development environment ready

## Key Activities

### 1. Project Scaffolding
Initialize the project structure:

```bash
{project-name}/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Route-level components
│   ├── services/       # API calls, business logic
│   ├── hooks/          # Custom React hooks
│   ├── utils/          # Helper functions
│   ├── types/          # TypeScript types/interfaces
│   └── styles/         # Global styles, themes
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── public/             # Static assets
├── docs/               # Project documentation
└── config files        # package.json, tsconfig, etc.
```

### 2. Development Workflow
Follow TDD approach:
1. **Write test** - Define expected behavior
2. **Run test** - Confirm it fails
3. **Write code** - Minimum to pass
4. **Run test** - Confirm it passes
5. **Refactor** - Improve without breaking

### 3. Code Organization Principles
- **Single Responsibility**: Each file does one thing
- **DRY**: Don't repeat yourself
- **KISS**: Keep it simple
- **Composition over inheritance**: Build from small pieces

### 4. Component Development Pattern
```typescript
// Example component structure
interface Props {
  data: DataType;
  onAction: (id: string) => void;
}

export function ComponentName({ data, onAction }: Props) {
  // 1. Hooks at top
  const [state, setState] = useState(initial);

  // 2. Derived state
  const computed = useMemo(() => transform(data), [data]);

  // 3. Effects
  useEffect(() => { /* side effects */ }, [deps]);

  // 4. Handlers
  const handleClick = () => onAction(data.id);

  // 5. Render
  return <div onClick={handleClick}>{computed}</div>;
}
```

### 5. API Development Pattern
```typescript
// RESTful endpoint structure
// GET    /api/resources      - List all
// GET    /api/resources/:id  - Get one
// POST   /api/resources      - Create
// PUT    /api/resources/:id  - Update
// DELETE /api/resources/:id  - Delete

// Example implementation
export async function getResources(filters: Filters): Promise<Resource[]> {
  const response = await fetch(`/api/resources?${buildQuery(filters)}`);
  if (!response.ok) throw new ApiError(response);
  return response.json();
}
```

### 6. Feature Implementation Checklist
For each feature:
- [ ] Write failing tests
- [ ] Implement feature
- [ ] Tests pass
- [ ] Add error handling
- [ ] Add loading states
- [ ] Add edge case handling
- [ ] Update types/interfaces
- [ ] Add inline documentation
- [ ] Manual testing complete

### 7. PR Creation
Create meaningful PRs with:

```markdown
## Summary
Brief description of changes

## Changes
- Added X component
- Modified Y service
- Fixed Z bug

## Testing
- [ ] Unit tests added
- [ ] Manual testing performed
- [ ] Edge cases covered

## Screenshots (if UI changes)
[Before/After images]
```

### 8. Code Quality Gates
Before committing:
- [ ] Linting passes (`npm run lint`)
- [ ] Tests pass (`npm run test`)
- [ ] Types check (`npm run typecheck`)
- [ ] No console.logs in production code
- [ ] No TODO comments without tickets

## Output Artifacts
- Working `src/` codebase
- Passing `tests/` suite
- PR descriptions documenting changes

## Development Commands
```bash
# Start development server
npm run dev

# Run tests
npm run test
npm run test:watch
npm run test:coverage

# Linting and formatting
npm run lint
npm run lint:fix
npm run format

# Type checking
npm run typecheck

# Build for production
npm run build
```

## Common Patterns

### State Management
```typescript
// Local state for component-specific
const [value, setValue] = useState(initial);

// Context for shared state
const AppContext = createContext<AppState>(defaultState);

// External store for complex state
// (Zustand, Redux, etc.)
```

### Error Handling
```typescript
try {
  const result = await riskyOperation();
  return { success: true, data: result };
} catch (error) {
  console.error('Operation failed:', error);
  return { success: false, error: formatError(error) };
}
```

### Loading States
```typescript
const { data, isLoading, error } = useQuery(key, fetcher);

if (isLoading) return <Skeleton />;
if (error) return <ErrorMessage error={error} />;
return <DataDisplay data={data} />;
```

## Git Workflow Integration

Development phase integrates with the **git-workflow** agent for version control.

### Starting a Feature

When entering Phase 6 for a new Feature PRD:

```bash
# git-workflow agent (branch mode) creates feature branch
git checkout -b feature/{feature-name}
```

### After Each User Story

When a story is marked complete in `progress.txt`:

1. **Orchestrator** detects completion
2. **git-workflow agent** (story-commit mode) is spawned
3. Agent runs verification:
   ```bash
   npm run lint && npm run typecheck && npm test
   ```
4. Agent stages and commits:
   ```bash
   git add .
   git commit -m "feat(scope): description

   Refs: US-XXX
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```
5. Agent updates `progress.txt`:
   ```
   [x] US-XXX: Story title - COMMITTED (abc1234)
   ```

### After Feature Complete

When all stories are committed:

1. **Orchestrator** runs gate-check
2. **git-workflow agent** (feature-pr mode) is spawned
3. Agent pushes and creates PR:
   ```bash
   git push -u origin feature/{feature-name}
   gh pr create --title "..." --body "..."
   ```
4. Agent returns PR URL to orchestrator

### Progress File Format

```
# Feature: {Feature Name}
# Branch: feature/{feature-name}

[x] US-001: First story - COMMITTED (abc1234)
[x] US-002: Second story - COMMITTED (def5678)
[ ] US-003: Third story - IN_PROGRESS
[ ] US-004: Fourth story - PENDING

# Status: 2/4 stories committed
# PR: Not yet created
```

### Manual Git Commands

If you need manual control:

```bash
# Manually commit current work
/commit "feat(scope): description"

# Manually create PR
/pr

# Check git status
git status
git log --oneline -5
```

### Conventional Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `test` | Adding/updating tests |
| `docs` | Documentation |
| `style` | Formatting only |
| `chore` | Build/tooling |

---

## Phase Gate Checklist
Before proceeding to Quality:
- [ ] All planned features implemented
- [ ] All stories committed (check progress.txt)
- [ ] Core tests passing
- [ ] No critical bugs
- [ ] Code reviewed (or self-reviewed)
- [ ] Basic error handling in place
- [ ] PR created (if feature complete)
