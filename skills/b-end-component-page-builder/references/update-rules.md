# Update Rules

Use this file whenever the task changes the component system.

## Decision Rules

### Add A New Variant

Choose a new variant when:

1. The structure stays the same
2. The component family already exists
3. The difference is mainly status, density, theme, or behavior

Examples:

1. New `Button` type
2. New `StatusTag` status
3. New `DataTable` interaction mode

### Add A New Component

Choose a new component when:

1. The structure is meaningfully different
2. The pattern is likely to be reused across pages
3. Existing component families cannot absorb it cleanly

Examples:

1. A new summary block with fixed internal layout
2. A new panel pattern reused across multiple modules

### Add A New Recipe

Choose a new recipe when:

1. Several components now combine in a repeatable page pattern
2. The page structure has become a stable archetype

Examples:

1. Approval workbench
2. Master-detail compare page

## Update Order

When the system changes, update in this order:

1. `references/component-system.md`
2. `references/page-recipes.md` if page assembly changed
3. `SKILL.md` only if the workflow or decision rules changed

## What To Record

For each new reusable addition, record:

1. Name
2. Purpose
3. Variants or states
4. Tokens touched
5. Page types that use it

## Quality Rules

1. Do not add one-off business styling as a shared component.
2. Do not fork near-duplicate components when a variant is enough.
3. Keep naming stable and short.
4. Prefer extending the current system over resetting it.
