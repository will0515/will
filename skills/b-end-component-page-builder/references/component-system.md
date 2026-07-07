# Component System

This reference is the working component system extracted from the Smart Service SVG pages.

## Foundations

### Core Colors

| Token | Value | Usage |
| --- | --- | --- |
| `color-primary-500` | `#0C9B72` | Primary action, active state, switch |
| `color-primary-100` | `#E8F8F3` | Active background, soft highlight |
| `color-primary-050` | `#F3FAF8` | Light table or panel tint |
| `color-text-primary` | `#2F2F2F` | Main text |
| `color-text-title` | `#222222` | Large titles |
| `color-text-secondary` | `#6F6A62` | Secondary text |
| `color-text-muted` | `#AAAAAA` | Hints |
| `color-text-placeholder` | `#CCCCCC` | Placeholder |
| `color-border-default` | `#E5EAE7` | Input and table border |
| `color-bg-page` | `#FBFAF8` | Page background |
| `color-bg-surface` | `#FFFFFF` | Panels and modals |
| `color-success-bg` | `#E0F4EF` | Success tag background |
| `color-warning` | `#E07F33` | Warning tag text |
| `color-warning-bg` | `#FEF0E5` | Warning tag background |
| `color-error` | `#E53E3E` | Error text and alerts |

### Typography

| Token | Value | Usage |
| --- | --- | --- |
| `font-family-base` | `Source Han Sans SC` | Main interface text |
| `font-family-number` | `Alibaba PuHuiTi 2.0` | Data and numeric emphasis |
| `font-size-xs` | `10px` | Tiny helper text |
| `font-size-sm` | `12px` | Secondary text |
| `font-size-md` | `14px` | Default content |
| `font-size-lg` | `16px` | Section emphasis |
| `font-size-xl` | `20px` | Page title or key data |

### Radius And Size

| Token | Value | Usage |
| --- | --- | --- |
| `radius-sm` | `5px` | Inputs, small controls |
| `radius-pill` | `12px` | Tags |
| `radius-round` | `15px` | 30x30 circular icon plate |
| `control-height-md` | `40px` | Default input and select |
| `tag-height` | `20px` | Status tag |
| `badge-size` | `20px` | Counter badge |
| `avatar-size-sm` | `30px` | Small avatar |

## Base Components

### Layout

1. `AppShell`
2. `Sidebar`
3. `SidebarBrand`
4. `SidebarSection`
5. `SidebarItem`
6. `SidebarProfileCard`
7. `ContentPanel`
8. `PageHeader`
9. `SectionHeader`
10. `SplitView`

### Form

1. `Form`
2. `FormField`
3. `TextInput`
4. `TextArea`
5. `Select`
6. `InputGroup`
7. `ReadonlyField`
8. `SearchField`
9. `HelperText`
10. `InlineErrorText`

### Data Display

1. `StatCard`
2. `InfoCard`
3. `TreeList`
4. `TreeNode`
5. `DataTable`
6. `TableToolbar`
7. `Pagination`
8. `StatusTag`
9. `Switch`
10. `Badge`

### Feedback And Action

1. `Modal`
2. `ConfirmDialog`
3. `Toast`
4. `EmptyState`
5. `InlineAlert`
6. `Button`
7. `IconButton`
8. `Checkbox`
9. `Radio`

## Business Components

1. `OrgDirectoryPanel`
2. `GroupMemberTable`
3. `ServiceAccessSummary`
4. `ServiceDetailForm`
5. `SdkInterfaceTable`
6. `SelectionSummaryCard`
7. `DangerConfirmDialog`

## Default Variants

### Button

1. `primary`
2. `secondary`
3. `danger`
4. `ghost`
5. `icon+text`

### StatusTag

1. `success`
2. `warning`
3. `default`

### Modal

1. `form-modal`
2. `selection-modal`
3. `confirm-modal`

### Table

1. `basic-table`
2. `selectable-table`
3. `switch-table`

### TreeNode

1. `default`
2. `expanded`
3. `collapsed`
4. `active`
5. `with-badge`

## Usage Rules

1. Reach for a layout recipe before inventing a custom page structure.
2. Use base components to form page skeletons.
3. Use business components when the pattern already matches.
4. Add a new component only if the pattern is clearly reusable.
