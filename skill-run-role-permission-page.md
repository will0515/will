# Skill 实跑结果

技能：
`$b-end-component-page-builder`

## 需求题目

角色权限配置页

## 需求描述

1. 页面用于后台管理员维护角色与权限
2. 左侧展示角色列表，支持搜索、新建角色
3. 右侧展示当前角色的基本信息、导航权限、操作权限、数据范围
4. 需要支持启用/停用角色
5. 需要支持保存修改、取消修改、删除角色
6. 需要有未保存离开确认、删除确认、空权限状态

## 页面目标

1. 让管理员快速定位角色并查看当前权限配置
2. 支持角色信息编辑和权限分配
3. 支持数据范围的精细配置
4. 保证保存、删除、离开等关键操作可控

## 页面结构

推荐命中 recipe：
`Tree And Detail Page`

页面结构建议：

1. `AppShell`
2. `PageHeader`
3. `ContentPanel`
4. `SplitView`
5. 左侧角色区：
   - `SectionHeader`
   - `SearchField`
   - `Button / primary`
   - `TreeList` 或 `RoleListPanel`
6. 右侧详情区：
   - `SectionHeader`
   - `Form`
   - `TextInput`
   - `Select`
   - `TextArea`
   - `InlineAlert`
7. 权限区：
   - `SectionHeader`
   - `PermissionTree`
   - `Checkbox`
8. 数据范围区：
   - `SectionHeader`
   - `Select`
   - `DataScopeCard`
9. 底部操作区：
   - `StickyActionBar`
   - `Button / primary`
   - `Button / secondary`
   - `Button / danger`
10. 反馈层：
   - `ConfirmDialog`
   - `Toast`
   - `EmptyState`

## 组件映射

| 页面区域 | 组件 |
| --- | --- |
| 页面骨架 | `AppShell` + `PageHeader` + `ContentPanel` |
| 左侧角色列表 | `SectionHeader` + `SearchField` + `Button` + `TreeList` |
| 角色基础信息 | `Form` + `FormField` + `TextInput` + `Select` + `TextArea` |
| 状态说明 | `InlineAlert` |
| 导航权限树 | `PermissionTree` + `Checkbox` |
| 数据范围配置 | `Select` + `InfoCard` 或 `DataScopeCard` |
| 底部保存操作 | `StickyActionBar` + `Button` |
| 删除和离开确认 | `ConfirmDialog` |
| 成功提示 | `Toast` |
| 空权限态 | `EmptyState` |

## 关键状态

1. 初始选中默认角色
2. 左侧搜索过滤角色
3. 角色停用态
4. 角色信息编辑中
5. 权限树部分勾选
6. 数据范围选择变化
7. 未保存离开确认
8. 删除角色确认
9. 空权限配置状态
10. 保存成功提示

## 需要补充的组件能力

1. `PermissionTree`
   - 用于权限分配的树形勾选组件
   - 支持父子联动、半选、展开收起
2. `RoleListPanel`
   - 用于角色管理的左侧列表面板
   - 兼容搜索、计数、新建入口、激活态
3. `StickyActionBar`
   - 用于详情页底部固定保存区
   - 支持主次危险操作并排
4. `DataScopeCard`
   - 用于展示数据范围说明和限制提示
5. `StatusTag / disabled`
   - 补一个“已停用”状态变体

## 默认假设

1. 页面面向系统管理员和权限管理员
2. 单次只编辑一个角色
3. 权限以导航树 + 操作点方式组合
4. 数据范围支持“全部数据 / 本部门 / 本部门及下级 / 指定组织”
5. 删除角色属于危险操作
6. 当前页面默认采用浅色 B 端风格

## 判断

这是一个适合沉淀进组件体系的真实页面。

原因：

1. 页面结构明确
2. 复用价值高
3. 能验证现有组件是否足够
4. 能暴露出新的高频业务组件需求
