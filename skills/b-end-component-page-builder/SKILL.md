---
name: b-end-component-page-builder
description: Build or update reusable B-end product pages from structured requirements and an evolving UI component system. Use when Codex needs to translate product requirements into page structure, component maps, page states, and front-end implementation; extend or normalize components, tokens, and variants; or keep future page work aligned with this user's private admin design system.
---

# B-end Component Page Builder

## Overview

Use this skill to turn product requirements into consistent B-end pages for a private component system owned by a UI designer. Reuse existing components first, extend existing families second, and create new components only when the new pattern is clearly reusable.

## Read These References

- Read `references/design-context.md` first.
- Read `references/component-system.md` before planning or implementing UI.
- Read `references/page-recipes.md` when the task is a common B-end page or modal.
- Read `references/update-rules.md` when the task changes the component system.

## Workflow

1. Extract the task frame.
   - Identify user role, business object, key actions, filters, batch actions, permissions, and page states.
   - Summarize the page goal in 3-6 bullets before designing or coding.
2. Build the page structure.
   - Match the requirement to the closest recipe.
   - Define page zones: shell, header, toolbar, filters, body, side panel, table, form, dialog, and feedback.
3. Map the requirement to components.
   - Compose from the existing component system first.
   - Prefer a new variant inside an existing family over a brand-new component.
   - Keep names aligned with the component reference.
4. Handle missing patterns.
   - If the missing pattern is likely cross-page or repeated, add it to the system instead of solving it only in the page.
   - Record purpose, states, tokens touched, and affected recipes.
5. Implement the page.
   - Default to `React + Vite + TypeScript` unless the repo already uses something else.
   - Build in this order: tokens, base components, composed business blocks, page assembly.
   - Keep the page practical, dense, and easy to scan.
6. Finish and normalize.
   - Verify empty, loading, error, disabled, selected, destructive, and success states when relevant.
   - Update the references if the task changed the system.

## Rules

- Keep the output in Chinese unless the repo or the user clearly wants English.
- Keep the default visual direction professional, calm, and efficient.
- Use the shared shell, shared spacing rhythm, and green-accent light theme unless the user asks for a different direction.
- Use existing tokens and component names whenever possible.
- Treat 40px as the default control height and 20px as the default tag or badge height unless a recipe says otherwise.
- Avoid page-specific one-off UI when a reusable component or recipe can absorb the requirement.
- Favor B-end clarity and maintainability over decorative treatment.

## Missing Input Handling

- If the requirement is incomplete, make minimal practical assumptions and label them clearly.
- Ask the user only when the missing information changes the page type, the core workflow, or the data permissions model.
- If the module name is clear but the fields are not, still output the page skeleton, component map, and the missing field list.
- If the requirement can map to an existing recipe, proceed with that recipe first.

## Output Templates

For planning tasks, use this structure:

1. `页面目标`
2. `页面结构`
3. `组件映射`
4. `关键状态`
5. `需要补充的组件能力`
6. `默认假设`

For implementation tasks, use this structure:

1. `实现范围`
2. `组件与 token 变更`
3. `页面代码`
4. `覆盖的状态`
5. `后续可继续沉淀的能力`

## Deliverables

When the user asks for planning only, return:

1. Page goal
2. Page structure
3. Component map
4. Key states
5. Needed additions to the component system

When the user asks for implementation, deliver:

1. Updated tokens or components if needed
2. Page code
3. Updated references when the system evolves
