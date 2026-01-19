# Backend Agent Handoff

**Task:** {{TASK_DESCRIPTION}}
**Timestamp:** {{TIMESTAMP}}
**Status:** {{COMPLETED / BLOCKED / NEEDS_REVIEW}}
**Agent Type:** {{Scala Backend / Python Backend}}

---

## Summary

{{BRIEF_SUMMARY_OF_WHAT_WAS_DONE}}

---

## Created/Modified Files

| File | Action | Description |
|------|--------|-------------|
| `{{path/to/Entity.scala}}` | Created | Entity model |
| `{{path/to/EntityDTO.scala}}` | Created | Data transfer object |
| `{{path/to/EntityService.scala}}` | Created | Business logic |
| `{{path/to/EntityController.scala}}` | Created | REST endpoints |

---

## API Contract

### Endpoints Created

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/{{resource}}` | {{Bearer/None}} | List all |
| `GET` | `/api/{{resource}}/{id}` | {{Bearer/None}} | Get by ID |
| `POST` | `/api/{{resource}}` | {{Bearer/None}} | Create new |
| `PUT` | `/api/{{resource}}/{id}` | {{Bearer/None}} | Full update |
| `PATCH` | `/api/{{resource}}/{id}` | {{Bearer/None}} | Partial update |
| `DELETE` | `/api/{{resource}}/{id}` | {{Bearer/None}} | Delete |

---

## Endpoint Details

### `{{METHOD}} {{PATH}}`

**Description:** {{what_this_endpoint_does}}

**Authentication:** {{Required / Optional / None}}
**Required Roles:** {{roles or "Any authenticated user"}}

#### Request

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `{{param}}` | `{{type}}` | {{description}} |

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `{{param}}` | `{{type}}` | {{yes/no}} | `{{default}}` | {{description}} |

**Request Body:**
```json
{
  "{{field}}": {{example_value}},
  "{{field}}": {{example_value}}
}
```

**Field Validation:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `{{field}}` | `{{type}}` | {{yes/no}} | {{min/max/pattern}} |

#### Response

**Success ({{STATUS_CODE}}):**
```json
{
  "{{field}}": {{example_value}},
  "{{field}}": {{example_value}}
}
```

**Error Responses:**
| Status | Code | When | Body |
|--------|------|------|------|
| 400 | `VALIDATION_ERROR` | Invalid input | `{"error": {"code": "...", "message": "...", "details": [...]}}` |
| 401 | `UNAUTHORIZED` | Missing/invalid token | `{"error": {"code": "UNAUTHORIZED", "message": "..."}}` |
| 403 | `FORBIDDEN` | Insufficient permissions | `{"error": {"code": "FORBIDDEN", "message": "..."}}` |
| 404 | `NOT_FOUND` | Resource doesn't exist | `{"error": {"code": "NOT_FOUND", "message": "..."}}` |
| 409 | `CONFLICT` | Duplicate/conflict | `{"error": {"code": "CONFLICT", "message": "..."}}` |

---

## For Frontend Agent

### API Integration Quick Reference

```typescript
// Base configuration
const API_BASE = '{{BASE_URL}}';
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`
};

// List {{resource}}s
GET {{BASE_URL}}/api/{{resource}}
Response: {{ResourceType}}[]

// Get single {{resource}}
GET {{BASE_URL}}/api/{{resource}}/{id}
Response: {{ResourceType}}

// Create {{resource}}
POST {{BASE_URL}}/api/{{resource}}
Body: {{CreateRequest}}
Response: {{ResourceType}}

// Update {{resource}}
PATCH {{BASE_URL}}/api/{{resource}}/{id}
Body: Partial<{{UpdateRequest}}>
Response: {{ResourceType}}

// Delete {{resource}}
DELETE {{BASE_URL}}/api/{{resource}}/{id}
Response: 204 No Content
```

### TypeScript Types

```typescript
interface {{ResourceType}} {
  id: {{number | string}};
  {{field}}: {{type}};
  {{field}}: {{type}};
  createdAt: string;
  updatedAt: string;
}

interface Create{{Resource}}Request {
  {{field}}: {{type}};
  {{field}}?: {{type}};  // Optional
}

interface Update{{Resource}}Request {
  {{field}}?: {{type}};
  {{field}}?: {{type}};
}

interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Array<{
      field: string;
      message: string;
    }>;
  };
}
```

### Form Validation (Client-Side)

| Field | Type | Required | Min | Max | Pattern |
|-------|------|----------|-----|-----|---------|
| `{{field}}` | `{{type}}` | {{yes/no}} | {{min}} | {{max}} | `{{regex}}` |

---

## Business Rules Implemented

### Validation Rules

- {{rule_description}}

### State Transitions

```
{{INITIAL_STATE}} → {{ALLOWED_TRANSITIONS}}
{{STATE}} → {{ALLOWED_TRANSITIONS}}
```

### Computed Fields

| Field | Computed From | Logic |
|-------|---------------|-------|
| `{{field}}` | `{{source_fields}}` | {{computation}} |

---

## Authentication & Authorization

### Auth Required Endpoints

| Endpoint | Auth | Roles |
|----------|------|-------|
| `{{endpoint}}` | {{type}} | {{roles}} |

### Token Format

```
Authorization: Bearer eyJhbGc...
```

### Permission Checks

- {{permission_description}}

---

## Dependencies

### New Dependencies Added

```
{{DEPENDENCY_NAME}} = {{VERSION}}
```

### External Services Called

| Service | Purpose | Config Key |
|---------|---------|------------|
| {{service}} | {{purpose}} | `{{env_var}}` |

---

## Testing Notes

### Unit Tests Created

| Test File | Coverage |
|-----------|----------|
| `{{test_file}}` | {{what_it_tests}} |

### Integration Tests

| Endpoint | Test Scenarios |
|----------|---------------|
| `{{endpoint}}` | {{scenarios}} |

### Test Data

```json
{{TEST_DATA_EXAMPLE}}
```

---

## Blockers / Questions

{{BLOCKERS_OR_QUESTIONS_FOR_ORCHESTRATOR}}

---

## Next Steps

1. Frontend Agent: Create `{{Component}}` to display {{resource}} list
2. Frontend Agent: Create `{{Form}}` with validation for create/edit
3. Frontend Agent: Add API hooks using `{{endpoint}}`
4. Test Generator: Create E2E tests for {{user_flow}}
