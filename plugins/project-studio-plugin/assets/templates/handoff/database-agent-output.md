# Database Agent Handoff

**Task:** {{TASK_DESCRIPTION}}
**Timestamp:** {{TIMESTAMP}}
**Status:** {{COMPLETED / BLOCKED / NEEDS_REVIEW}}

---

## Summary

{{BRIEF_SUMMARY_OF_WHAT_WAS_DONE}}

---

## Created Files

| File | Action | Description |
|------|--------|-------------|
| `{{MIGRATION_PATH}}/V{{VERSION}}__{{description}}.sql` | Created | {{purpose}} |

---

## Schema Changes

### Tables Created

| Table | Purpose | Primary Key |
|-------|---------|-------------|
| `{{table_name}}` | {{purpose}} | `{{pk_column}}` |

### Columns Added/Modified

| Table | Column | Type | Constraints | Notes |
|-------|--------|------|-------------|-------|
| `{{table}}` | `{{column}}` | `{{type}}` | `{{constraints}}` | {{notes}} |

### Relationships

| Parent Table | Child Table | Type | Foreign Key |
|--------------|-------------|------|-------------|
| `{{parent}}` | `{{child}}` | {{1:N / M:N}} | `{{fk_column}}` |

### Indexes Created

| Index Name | Table | Columns | Type |
|------------|-------|---------|------|
| `idx_{{table}}_{{column}}` | `{{table}}` | `{{columns}}` | {{BTREE/HASH/GIN}} |

---

## For Backend Agent

Use this information when creating entity classes and repositories.

### Entity Mapping

```
Table: {{table_name}}
├── id ({{type}}) → id: {{LangType}}
├── {{column}} ({{sql_type}}) → {{fieldName}}: {{LangType}}
├── {{column}} ({{sql_type}}) → {{fieldName}}: {{LangType}}
└── {{fk_column}} ({{sql_type}}) → {{relationField}}: {{EntityType}}
```

### Column-to-Field Reference

| Column | Field Name | Type | Nullable | Default |
|--------|------------|------|----------|---------|
| `{{column}}` | `{{fieldName}}` | `{{type}}` | {{yes/no}} | `{{default}}` |

### Relationship Annotations

```
{{table}} → {{related_table}}
Type: {{ManyToOne / OneToMany / ManyToMany}}
Join: {{join_column or join_table}}
Fetch: {{LAZY / EAGER recommended}}
```

---

## For Frontend Agent

Use this for form validation and display formatting.

### Form Fields

| Field | Display Label | Type | Required | Validation |
|-------|---------------|------|----------|------------|
| `{{field}}` | {{label}} | {{input_type}} | {{yes/no}} | {{rules}} |

### Display Formatting

| Field | Format | Notes |
|-------|--------|-------|
| `{{field}}` | {{format_hint}} | {{display_notes}} |

---

## Data Constraints

### Business Rules Enforced at DB Level

- {{constraint_description}}

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| `{{field}}` | {{rule}} | {{message}} |

---

## Migration Details

### Forward Migration

```sql
{{MIGRATION_SQL}}
```

### Rollback Instructions

```sql
{{ROLLBACK_SQL}}
```

### Data Migration Notes

{{NOTES_ABOUT_DATA_MIGRATION_IF_ANY}}

---

## Testing Notes

### Seed Data Provided

- Location: `{{seed_file_path}}`
- Records: {{count}} test records

### Test Scenarios

- {{scenario_1}}
- {{scenario_2}}

---

## Blockers / Questions

{{BLOCKERS_OR_QUESTIONS_FOR_ORCHESTRATOR}}

---

## Next Steps

1. Backend Agent: Create `{{Entity}}` entity matching this schema
2. Backend Agent: Create `{{Entity}}Repository` with custom queries for `{{use_case}}`
3. Frontend Agent: Create form with fields: `{{field_list}}`
