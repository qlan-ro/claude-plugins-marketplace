# Phase 4: Infer Design

## Objective
Document the existing design system and UI patterns by analyzing the codebase. This is documentation, not redesign.

## Entry Criteria
- Codebase Analysis complete
- Architecture documented

## Why This Phase Matters
New UI must match existing design. Documenting what exists:
- Ensures visual consistency
- Provides component references for Feature PRDs
- Prevents creating duplicate components

---

## Key Activities

### 1. Extract Design Tokens

**From Tailwind config:**
```javascript
// tailwind.config.js
theme: {
  colors: {
    primary: '#3B82F6',
    secondary: '#6B7280',
    ...
  },
  spacing: { ... },
  borderRadius: { ... }
}
```

**From CSS variables:**
```css
:root {
  --color-primary: #3B82F6;
  --radius-md: 8px;
}
```

**Output:**
```markdown
## Design Tokens

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| primary | #3B82F6 | Buttons, links, accents |
| secondary | #6B7280 | Secondary text, borders |
| background | #FFFFFF | Page background |
| surface | #F9FAFB | Cards, elevated surfaces |
| text-primary | #111827 | Main text |
| text-secondary | #6B7280 | Supporting text |
| error | #EF4444 | Error states |
| success | #10B981 | Success states |
| warning | #F59E0B | Warning states |

### Typography
| Token | Value | Usage |
|-------|-------|-------|
| font-sans | Inter, system-ui | Body text |
| text-xs | 12px | Labels, captions |
| text-sm | 14px | Secondary text |
| text-base | 16px | Body text |
| text-lg | 18px | Large body |
| text-xl | 20px | Subheadings |
| text-2xl | 24px | Section titles |
| text-3xl | 30px | Page titles |

### Spacing
| Token | Value | Usage |
|-------|-------|-------|
| 1 | 4px | Tight spacing |
| 2 | 8px | Component internal |
| 4 | 16px | Between elements |
| 6 | 24px | Section spacing |
| 8 | 32px | Major sections |

### Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| sm | 4px | Buttons, inputs |
| md | 8px | Cards |
| lg | 16px | Modals |
| full | 9999px | Avatars, pills |
```

### 2. Document Component Library

**Inventory existing UI components:**

```markdown
## Component Library

### Source
- Library: shadcn/ui (or custom)
- Location: `src/components/ui/`

### Available Components

#### Buttons
| Variant | Class/Props | Usage |
|---------|-------------|-------|
| Primary | `variant="default"` | Main actions |
| Secondary | `variant="secondary"` | Secondary actions |
| Ghost | `variant="ghost"` | Subtle actions |
| Destructive | `variant="destructive"` | Delete, danger |

**Example:**
```tsx
<Button variant="default" size="md">
  Save Changes
</Button>
```

#### Form Elements
| Component | Location | Features |
|-----------|----------|----------|
| Input | ui/Input.tsx | Text, password, email |
| Select | ui/Select.tsx | Dropdown selection |
| Checkbox | ui/Checkbox.tsx | Boolean toggle |
| Textarea | ui/Textarea.tsx | Multi-line text |

#### Layout
| Component | Location | Usage |
|-----------|----------|-------|
| Card | ui/Card.tsx | Content container |
| Dialog | ui/Dialog.tsx | Modal dialogs |
| Sheet | ui/Sheet.tsx | Slide-over panels |
| Tabs | ui/Tabs.tsx | Tabbed content |

#### Feedback
| Component | Location | Usage |
|-----------|----------|-------|
| Toast | ui/Toast.tsx | Notifications |
| Alert | ui/Alert.tsx | Inline messages |
| Badge | ui/Badge.tsx | Status indicators |
| Skeleton | ui/Skeleton.tsx | Loading states |
```

### 3. Document Page Layouts

**Extract layout patterns:**

```markdown
## Page Layouts

### Main Layout
**File:** `src/components/layout/MainLayout.tsx`

```
┌─────────────────────────────────────────┐
│  Header (fixed)                         │
├──────────┬──────────────────────────────┤
│          │                              │
│ Sidebar  │       Main Content           │
│  (240px) │                              │
│          │                              │
│          │                              │
└──────────┴──────────────────────────────┘
```

### Auth Layout
**File:** `src/components/layout/AuthLayout.tsx`

```
┌─────────────────────────────────────────┐
│                                         │
│          ┌───────────────┐              │
│          │  Auth Card    │              │
│          │  (max-w-md)   │              │
│          └───────────────┘              │
│                                         │
└─────────────────────────────────────────┘
```

### Existing Pages
| Page | Path | Layout |
|------|------|--------|
| Login | /login | AuthLayout |
| Register | /register | AuthLayout |
| Dashboard | /dashboard | MainLayout |
| Profile | /profile | MainLayout |
| Settings | /settings | MainLayout |
```

### 4. Document Navigation

```markdown
## Navigation

### Primary Navigation
**Location:** Header or Sidebar
**Component:** `src/components/layout/Sidebar.tsx`

| Item | Path | Icon | Auth Required |
|------|------|------|---------------|
| Dashboard | /dashboard | HomeIcon | Yes |
| Posts | /posts | FileTextIcon | Yes |
| Settings | /settings | SettingsIcon | Yes |

### User Menu
**Location:** Header right
**Component:** `src/components/layout/UserMenu.tsx`

| Item | Action |
|------|--------|
| Profile | Navigate to /profile |
| Settings | Navigate to /settings |
| Logout | Clear session, redirect |
```

### 5. Document Existing Screens

**Screenshot or describe key screens:**

```markdown
## Existing Screens

### Dashboard
**Path:** /dashboard
**File:** `src/pages/Dashboard.tsx`

```
┌─────────────────────────────────────────┐
│  Dashboard                    [+ New]   │
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Stat 1  │ │ Stat 2  │ │ Stat 3  │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│                                         │
│  Recent Activity                        │
│  ├─ Item 1                              │
│  ├─ Item 2                              │
│  └─ Item 3                              │
└─────────────────────────────────────────┘
```

**Components used:**
- StatCard (ui/StatCard.tsx)
- ActivityList (features/ActivityList.tsx)

### Profile
**Path:** /profile
**File:** `src/pages/Profile.tsx`

{Similar wireframe}
```

### 6. Document Responsive Behavior

```markdown
## Responsive Design

### Breakpoints
| Name | Width | Behavior |
|------|-------|----------|
| sm | 640px | Mobile |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Large desktop |

### Responsive Patterns

| Component | Mobile | Desktop |
|-----------|--------|---------|
| Sidebar | Hidden (hamburger) | Visible |
| Navigation | Bottom tabs | Side nav |
| Cards | Single column | Grid |
| Tables | Card list | Full table |
```

---

## Output Artifact

Create `docs/DESIGN.md`:

```markdown
# Design Specification: {PROJECT_NAME}

**Inferred from codebase:** {DATE}
**Status:** Documentation of existing design

---

## Design Tokens

{From Section 1}

---

## Component Library

{From Section 2}

---

## Page Layouts

{From Section 3}

---

## Navigation

{From Section 4}

---

## Existing Screens

{From Section 5}

---

## Responsive Design

{From Section 6}

---

## Guidelines for New UI

When adding new features, follow these patterns:

### Adding a New Page
1. Use appropriate layout (MainLayout, AuthLayout)
2. Follow existing page structure
3. Use existing components from ui/

### Adding a New Component
1. Check if ui/ component exists first
2. Follow design token usage
3. Ensure responsive behavior

### Adding to Navigation
1. Add to Sidebar.tsx or Header.tsx
2. Follow existing icon + label pattern
3. Update mobile navigation if applicable
```

---

## Phase Gate Checklist

Before proceeding to Planning (Feature PRDs):
- [ ] Design tokens extracted
- [ ] Component library documented
- [ ] Page layouts documented
- [ ] Navigation patterns documented
- [ ] Existing screens documented
- [ ] Responsive patterns documented
- [ ] `docs/DESIGN.md` created
- [ ] User has confirmed design accuracy
