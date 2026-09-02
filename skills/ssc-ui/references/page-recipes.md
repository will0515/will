# Page Recipes

Use these recipes as the default assembly patterns for B-end page work.

## 1. List Page

Use for management, configuration, and entity browsing.

### Structure

1. `AppShell`
2. `PageHeader`
3. `ContentPanel`
4. `SectionHeader` or `TableToolbar`
5. Filter row with `SearchField`, `Select`, `Button`
6. `DataTable`
7. `Pagination`

### Required States

1. Empty
2. Loading
3. Search or filter active
4. Batch selection if relevant
5. Delete or destructive confirmation if relevant

## 2. Detail Page

Use for service detail, configuration detail, and record detail.

### Structure

1. `AppShell`
2. `PageHeader`
3. `ContentPanel`
4. Multiple `SectionHeader` blocks
5. `Form` with `ReadonlyField`, `TextInput`, `Select`, `TextArea`
6. Related `DataTable` if child records exist

### Required States

1. Readonly
2. Editable
3. Disabled fields
4. Unsaved change confirmation
5. Inline error or restriction prompt

## 3. Tree And Detail Page

Use for organization, permission, catalog, and processing group pages.

### Structure

1. `AppShell`
2. `PageHeader`
3. `ContentPanel`
4. `SplitView`
5. Left: `OrgDirectoryPanel`
6. Right: `InfoCard`, `Form`, or `DataTable`

### Required States

1. Root selected
2. Child selected
3. Expanded and collapsed nodes
4. Empty right panel
5. Empty left panel

## 4. Dashboard Summary Plus Table

Use for overview pages with KPI cards and downstream lists.

### Structure

1. `AppShell`
2. `PageHeader`
3. `ContentPanel`
4. `ServiceAccessSummary` or `StatCard` row
5. `SectionHeader`
6. `DataTable`
7. `Pagination`

### Required States

1. Metric cards loaded
2. Metric cards empty
3. Table empty
4. Status tag combinations

## 5. Create Or Edit Modal

Use for lightweight creation and editing without navigation.

### Structure

1. `Modal`
2. `SectionHeader` or title row
3. `Form`
4. `TextInput`, `Select`, `TextArea`
5. Footer action buttons

### Required States

1. Required field empty
2. Readonly field
3. Validation error
4. Submit disabled

## 6. Selection Modal

Use for member selection, owner selection, and related-object picking.

### Structure

1. `selection-modal`
2. Summary area with current object and selected count
3. Optional filter row
4. `selectable-table`
5. `Pagination`
6. Footer actions

### Required States

1. Nothing selected
2. One selected
3. Multiple selected
4. Cross-page selection if relevant

## 7. Confirm And Feedback

Use for delete, leave, close, and forbidden operations.

### Structure

1. `ConfirmDialog` for decisions
2. `Toast` for lightweight result feedback
3. `InlineAlert` for contextual restrictions

### Required States

1. Neutral confirmation
2. Dangerous confirmation
3. Success feedback
4. Warning feedback
5. Error feedback

## 8. Dashboard Card Interpretation Editor

Use for editing the explanatory text attached to dashboard cards and reports.

### Structure

1. `AppShell`
2. `PageHeader`
3. `ContentPanel`
4. `SplitView`
5. Left: dashboard card list and status filters
6. Right: card title and `StatusTag`
7. `Select` for interpretation type
8. `RichTextEditor`
9. Save metadata and primary `Button`

### Required States

1. Existing interpretation loaded
2. Empty interpretation
3. Dirty draft
4. Saved successfully
5. Readonly or published content
