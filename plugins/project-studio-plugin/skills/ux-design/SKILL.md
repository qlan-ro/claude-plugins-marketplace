---
name: ux-design
description: |
  UX/UI design specifications for developer handoff. Use this skill when:
  - Mapping user flows and journeys
  - Creating screen inventories
  - Defining design systems (tokens, components)
  - Planning responsive behavior

  This skill is domain-specific - it knows HOW to design UX, not workflow phases.
---

# UX Design

Create developer-ready design specifications.

## Design Document Sections

### 1. User Flows

Map how users accomplish goals:

```markdown
## User Flows

### Primary Flow: {Goal Name}

```
[Landing] → [Sign Up] → [Onboarding] → [Dashboard]
               ↓
           [Login] ←────────────────────┘
```

| Step | Screen | User Action | System Response |
|------|--------|-------------|-----------------|
| 1 | Landing | Clicks "Get Started" | Shows signup form |
| 2 | Signup | Enters email/password | Validates, creates account |
| 3 | Onboarding | Completes profile | Saves preferences |
| 4 | Dashboard | Views main interface | Shows personalized data |
```

### 2. Screen Inventory

List all screens needed:

```markdown
## Screen Inventory

### Public Screens (No Auth)
| Screen | URL | Purpose | Key Components |
|--------|-----|---------|----------------|
| Landing | / | Convert visitors | Hero, Features, CTA |
| Login | /login | Authenticate | LoginForm |
| Signup | /signup | Create accounts | SignupForm |

### Protected Screens (Auth Required)
| Screen | URL | Purpose | Key Components |
|--------|-----|---------|----------------|
| Dashboard | /dashboard | Main workspace | Sidebar, Stats, Feed |
| Settings | /settings | User preferences | SettingsTabs, Forms |
| Profile | /profile | User info | ProfileCard, EditForm |
```

### 3. Wireframes

ASCII wireframes for key screens:

```markdown
### Dashboard Wireframe
```
┌─────────────────────────────────────────────────────┐
│ [Logo]            Search...          [User Avatar ▼]│
├────────────┬────────────────────────────────────────┤
│            │  Welcome back, {name}                  │
│  Dashboard │  ┌────────┐ ┌────────┐ ┌────────┐     │
│  Projects  │  │ Stat 1 │ │ Stat 2 │ │ Stat 3 │     │
│  Settings  │  └────────┘ └────────┘ └────────┘     │
│            │                                        │
│            │  Recent Activity                       │
│            │  ┌──────────────────────────────┐     │
│            │  │ Item 1                   ... │     │
│            │  │ Item 2                   ... │     │
│            │  └──────────────────────────────┘     │
└────────────┴────────────────────────────────────────┘
```
```

### 4. Design Tokens

```markdown
## Design Tokens

### Colors

#### Brand
| Token | Value | Usage |
|-------|-------|-------|
| --color-primary | #3B82F6 | Primary actions, links |
| --color-primary-hover | #2563EB | Hover states |

#### Neutral
| Token | Value | Usage |
|-------|-------|-------|
| --color-bg | #FFFFFF | Page background |
| --color-surface | #F9FAFB | Card backgrounds |
| --color-border | #E5E7EB | Borders, dividers |
| --color-text | #111827 | Primary text |
| --color-text-muted | #6B7280 | Secondary text |

#### Semantic
| Token | Value | Usage |
|-------|-------|-------|
| --color-error | #EF4444 | Errors, destructive |
| --color-warning | #F59E0B | Warnings |
| --color-success | #10B981 | Success states |

### Typography
| Token | Value | Usage |
|-------|-------|-------|
| --font-family | Inter, system-ui | All text |
| --font-size-sm | 0.875rem | Secondary text |
| --font-size-base | 1rem | Body text |
| --font-size-lg | 1.125rem | Large body |
| --font-size-xl | 1.25rem | Subheadings |
| --font-size-2xl | 1.5rem | Headings |

### Spacing
| Token | Value | Usage |
|-------|-------|-------|
| --space-1 | 0.25rem | Tight |
| --space-2 | 0.5rem | Small gaps |
| --space-4 | 1rem | Standard |
| --space-6 | 1.5rem | Section spacing |
| --space-8 | 2rem | Large sections |

### Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| --radius-sm | 0.25rem | Small elements |
| --radius-md | 0.375rem | Buttons, inputs |
| --radius-lg | 0.5rem | Cards |
| --radius-full | 9999px | Pills, avatars |
```

### 5. Component Library

```markdown
## Components

### Approach: {shadcn/ui / Radix / Custom}

### Button
| Variant | Usage |
|---------|-------|
| Primary | Main CTAs |
| Secondary | Secondary actions |
| Ghost | Tertiary actions |
| Destructive | Delete, remove |

Sizes: sm (32px), md (40px), lg (48px)
States: default, hover, active, disabled

### Input
| Variant | Usage |
|---------|-------|
| Text | Standard input |
| Email | With validation |
| Password | Hidden with toggle |
| Textarea | Multi-line |

States: default, focus, error, disabled

### Card
- Header (optional)
- Body (required)
- Footer (optional)
- Variants: elevated, outlined, flat

### Modal
- Overlay background
- Centered content
- Close button (X)
- Sizes: sm (400px), md (500px), lg (600px)

### Layout Components
| Component | Purpose |
|-----------|---------|
| Container | Max-width wrapper |
| Stack | Vertical flex |
| Row | Horizontal flex |
| Grid | CSS grid |
| Sidebar | Collapsible nav |
```

### 6. Navigation

```markdown
## Navigation

### Primary Nav (Sidebar)
```
├── Dashboard (home icon)
├── {Feature 1} (icon)
│   ├── Sub-item 1
│   └── Sub-item 2
├── {Feature 2} (icon)
└── Settings (cog icon)
```

### User Menu
```
├── Profile
├── Preferences
├── ─────────
└── Sign Out
```

### Breadcrumbs
`Home / Section / Page`
```

### 7. Responsive Behavior

```markdown
## Responsive Design

### Breakpoints
| Name | Width | Device |
|------|-------|--------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablets |
| lg | 1024px | Small laptops |
| xl | 1280px | Desktops |

### Layout Adaptations

#### Sidebar
| Breakpoint | Behavior |
|------------|----------|
| < md | Hidden, hamburger menu |
| md - lg | Icons only |
| > lg | Full with labels |

#### Content Grid
| Breakpoint | Columns |
|------------|---------|
| < sm | 1 |
| sm - md | 2 |
| md - xl | 3 |
| > xl | 4 |
```

## Output Template

Create `docs/DESIGN.md` with the sections above.

## Continue-Project Mode (Extraction)

When documenting an EXISTING codebase:

1. **Extract existing tokens** - Find CSS variables, Tailwind config
2. **Inventory existing components** - List what's built
3. **Document patterns** - How layouts work now
4. **Note inconsistencies** - Design debt

```bash
# Find existing design tokens
grep -r "var(--" --include="*.css"
cat tailwind.config.js | grep -A 20 "colors:"

# Find components
find . -path "*/components/*" -name "*.tsx" | head -30
```

## Design Checklist

Before finalizing, ensure:
- [ ] All PRD features have corresponding screens
- [ ] User can accomplish primary goals via flows
- [ ] Tokens cover all color/spacing/typography needs
- [ ] Components cover all UI patterns
- [ ] Responsive behavior defined
- [ ] Navigation structure clear

## Add-Feature Mode (Amendment)

When adding features via `/add-feature` that require design changes:

### Rules for Amendment Mode

1. **DO NOT recreate** the design system
2. **READ** existing DESIGN.md first
3. **PRESERVE** all existing tokens, components, flows
4. **ADD** new sections for new screens/components
5. **EXTEND** existing patterns (don't replace)
6. **UPDATE** token lists only if theme changes

### Process

1. **Identify what's needed:**
   - New screens/pages?
   - New components?
   - New user flows?
   - New design tokens?

2. **Add new sections:**
```markdown
## Design Amendments (Added {date})

### New Feature: {Feature Name}

#### New Screens
| Screen | URL | Purpose | Components Used |
|--------|-----|---------|-----------------|
| Theme Settings | /settings/theme | Toggle dark mode | ThemeToggle, Card |

#### New Components

##### ThemeToggle
- Purpose: Switch between light/dark modes
- States: light (sun icon), dark (moon icon)
- Size: 40px touch target
- Location: Settings page, User menu

#### New User Flow
```
[Settings] → [Theme Settings] → [Toggle] → [Apply Theme]
                                    ↓
                              [Toast: "Theme updated"]
```

#### Token Additions (Dark Theme)
| Token | Light Value | Dark Value |
|-------|-------------|------------|
| --color-bg | #FFFFFF | #1A1A2E |
| --color-surface | #F9FAFB | #16162D |
| --color-text | #111827 | #EAEAEA |
```

3. **Note impacts on existing:**
```markdown
#### Impacts on Existing
- **All components:** Add dark mode variant support
- **Layout:** No changes needed
- **Navigation:** Add theme toggle to user menu
```

### Common Feature Design Patterns

| Feature | Typically Needs |
|---------|-----------------|
| Dark mode | Token additions (dark values), ThemeToggle component |
| PDF export | Export button, Progress indicator, Download modal |
| Notifications | NotificationBell, NotificationPanel, Toast |
| Search | SearchInput, SearchResults, Empty state |
| Filters | FilterBar, FilterChip, ActiveFilters |
| File upload | DropZone, ProgressBar, FilePreview |

### Output

Updated `docs/DESIGN.md` with:
- New sections for additional screens/components
- New flows for feature-specific journeys
- Existing content UNCHANGED (unless directly affected)
- Clear separation of amendments from original
