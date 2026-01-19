# Frontend Agent Handoff

**Task:** {{TASK_DESCRIPTION}}
**Timestamp:** {{TIMESTAMP}}
**Status:** {{COMPLETED / BLOCKED / NEEDS_REVIEW}}
**Framework:** {{React / Angular / Vue}}

---

## Summary

{{BRIEF_SUMMARY_OF_WHAT_WAS_DONE}}

---

## Created/Modified Files

| File | Action | Description |
|------|--------|-------------|
| `src/components/{{Component}}/{{Component}}.tsx` | Created | Main component |
| `src/components/{{Component}}/index.ts` | Created | Export barrel |
| `src/pages/{{Page}}.tsx` | Created | Page component |
| `src/hooks/use{{Feature}}.ts` | Created | Data fetching hook |
| `src/services/{{feature}}Api.ts` | Created | API service |
| `src/types/{{feature}}.ts` | Created | TypeScript types |

---

## Components Created

### Component Hierarchy

```
{{ParentComponent}}
├── {{ChildComponent1}}
│   └── {{GrandchildComponent}}
├── {{ChildComponent2}}
└── {{ChildComponent3}}
```

### Component Details

| Component | Type | Props | Purpose |
|-----------|------|-------|---------|
| `{{ComponentName}}` | {{Presentational/Container}} | `{{props}}` | {{purpose}} |

### Component Props Interface

```typescript
interface {{Component}}Props {
  {{prop}}: {{type}};
  {{prop}}?: {{type}};  // Optional
  on{{Event}}: ({{params}}) => void;
}
```

---

## Routes Created

| Route | Component | Auth | Description |
|-------|-----------|------|-------------|
| `/{{path}}` | `{{Component}}` | {{yes/no}} | {{description}} |
| `/{{path}}/:id` | `{{Component}}` | {{yes/no}} | {{description}} |

### Route Configuration

```typescript
// React Router example
{
  path: '/{{path}}',
  element: <{{Component}} />,
  children: [
    { path: ':id', element: <{{DetailComponent}} /> }
  ]
}
```

---

## API Integration

### Hooks Created

| Hook | Endpoint | Method | Returns |
|------|----------|--------|---------|
| `use{{Resource}}s()` | `/api/{{resource}}` | GET | `{ data, isLoading, error }` |
| `use{{Resource}}(id)` | `/api/{{resource}}/{id}` | GET | `{ data, isLoading, error }` |
| `useCreate{{Resource}}()` | `/api/{{resource}}` | POST | `{ mutate, isPending }` |
| `useUpdate{{Resource}}()` | `/api/{{resource}}/{id}` | PATCH | `{ mutate, isPending }` |
| `useDelete{{Resource}}()` | `/api/{{resource}}/{id}` | DELETE | `{ mutate, isPending }` |

### API Service Functions

```typescript
// {{feature}}Api.ts
export const {{feature}}Api = {
  getAll: () => apiClient.get<{{Type}}[]>('/api/{{resource}}'),
  getById: (id: string) => apiClient.get<{{Type}}>(`/api/{{resource}}/${id}`),
  create: (data: Create{{Type}}Request) => apiClient.post<{{Type}}>('/api/{{resource}}', data),
  update: (id: string, data: Update{{Type}}Request) => apiClient.patch<{{Type}}>(`/api/{{resource}}/${id}`, data),
  delete: (id: string) => apiClient.delete(`/api/{{resource}}/${id}`),
};
```

---

## State Management

### Store/Context Created

| Store | Purpose | Key State |
|-------|---------|-----------|
| `{{StoreName}}` | {{purpose}} | `{{state_description}}` |

### State Shape

```typescript
interface {{Feature}}State {
  {{field}}: {{type}};
  {{field}}: {{type}};
  isLoading: boolean;
  error: Error | null;
}
```

### Actions/Reducers

| Action | Payload | Effect |
|--------|---------|--------|
| `{{ACTION_TYPE}}` | `{{payload_type}}` | {{effect}} |

---

## User Flows Implemented

### Happy Path: {{Flow Name}}

1. User navigates to `{{route}}`
2. Page loads, shows loading spinner
3. Data fetches successfully
4. User sees `{{what_they_see}}`
5. User clicks `{{action}}`
6. {{result}}

### Loading State

- Component: `{{LoadingComponent}}`
- Shows: {{what_shows}}
- Duration: Until API responds

### Error State

- Component: `{{ErrorComponent}}`
- Shows: {{error_message}}
- Actions: {{retry_button, etc}}

### Empty State

- Component: `{{EmptyComponent}}`
- Shows: {{empty_message}}
- Actions: {{cta_button}}

---

## Form Implementation

### Form Fields

| Field | Input Type | Validation | Error Message |
|-------|------------|------------|---------------|
| `{{field}}` | `{{text/select/date}}` | `{{rules}}` | `{{message}}` |

### Form Schema (Zod/Yup)

```typescript
const {{form}}Schema = z.object({
  {{field}}: z.string().min(1, '{{error_message}}'),
  {{field}}: z.number().positive(),
  {{field}}: z.string().email(),
});
```

### Form State

```typescript
const defaultValues = {
  {{field}}: '',
  {{field}}: 0,
};
```

---

## Styling

### Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| `{{color}}` | `{{value}}` | {{where_used}} |
| `{{spacing}}` | `{{value}}` | {{where_used}} |

### CSS Classes / Tailwind

```css
/* Key classes used */
.{{class-name}} { /* {{purpose}} */ }
```

### Responsive Breakpoints

| Breakpoint | Layout Change |
|------------|---------------|
| `sm` (640px) | {{change}} |
| `md` (768px) | {{change}} |
| `lg` (1024px) | {{change}} |

---

## Accessibility

### ARIA Labels

| Element | Label | Purpose |
|---------|-------|---------|
| `{{element}}` | `{{label}}` | {{purpose}} |

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | {{action}} |
| `Enter` | {{action}} |
| `Escape` | {{action}} |

### Screen Reader Support

- {{accessibility_feature}}

---

## For Test Generator

### Components to Test

| Component | Test Priority | Key Scenarios |
|-----------|---------------|---------------|
| `{{Component}}` | High | {{scenarios}} |

### User Interactions to Test

1. {{interaction_description}}
2. {{interaction_description}}

### API Mocks Needed

```typescript
const mock{{Resource}}s = [
  { id: '1', {{field}}: {{value}} },
  { id: '2', {{field}}: {{value}} },
];
```

### Test IDs Added

| Element | Test ID | Purpose |
|---------|---------|---------|
| `{{element}}` | `{{test-id}}` | {{for_what_test}} |

---

## For Code Reviewer

### Key Decisions Made

- {{decision_and_rationale}}

### Performance Considerations

- {{optimization_applied}}

### Known Limitations

- {{limitation}}

---

## Blockers / Questions

{{BLOCKERS_OR_QUESTIONS_FOR_ORCHESTRATOR}}

---

## Next Steps

1. Test Generator: Create unit tests for `{{Component}}`
2. Test Generator: Create E2E test for `{{user_flow}}`
3. Code Reviewer: Review component structure
4. Doc Writer: Update user guide with new feature
