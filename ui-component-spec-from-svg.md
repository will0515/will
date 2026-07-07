# Smart Service UI 组件整理

基于目录 `/Users/edy/Desktop/ssc效果图-svg/` 中 20 张 SVG 页面整理。

说明：颜色、字体、字号来自 SVG 统计；阴影、部分大容器圆角和间距为基于页面视觉的整理建议，后续可结合 Sketch 原文件再精修。

## 1. 页面范围

本次页面主要来自 4 个业务模块：

1. 组织架构
2. 处理组
3. 系统列表
4. 系列列表

对应页面类型主要有：

1. 列表页
2. 详情页
3. 表单弹窗
4. 选择弹窗
5. 二次确认弹窗
6. 全局提示
7. 空状态

---

## 2. 组件拆分建议

建议拆成两层：

1. 基础组件
2. 业务组件

### 2.1 基础组件

#### A. 布局类

| 组件名 | 用途 | 主要变体/状态 |
| --- | --- | --- |
| `AppShell` | 整体应用框架，左侧导航 + 右侧内容区 | 默认 |
| `Sidebar` | 左侧导航容器 | 展开 |
| `SidebarBrand` | Logo + 系统名称 | 默认 |
| `SidebarSection` | 左侧一级分组，如“人员与组织” | 默认 / 展开 |
| `SidebarItem` | 左侧菜单项 | 默认 / 激活 / 带图标 |
| `SidebarProfileCard` | 左下角用户信息卡片 | 默认 |
| `ContentPanel` | 右侧主内容白色卡片容器 | 默认 |
| `PageHeader` | 页面标题区 | 仅标题 / 返回+标题 / 标题+状态 |
| `SectionHeader` | 分区标题，如“基本信息”“成员列表” | 默认 / 带操作 |
| `SplitView` | 左右分栏内容布局 | `40/60` / `50/50` |

#### B. 表单类

| 组件名 | 用途 | 主要变体/状态 |
| --- | --- | --- |
| `Form` | 表单容器 | 单列 / 双列 |
| `FormField` | 标签 + 控件组合 | 默认 / 必填 / 说明文案 / 错误 |
| `TextInput` | 单行输入框 | 默认 / 占位 / 只读 / 禁用 / 错误 |
| `TextArea` | 多行输入 | 默认 / 占位 / 只读 |
| `Select` | 下拉选择 | 默认 / 已选 / 禁用 |
| `InputGroup` | 两列字段组合 | 左右并排 |
| `ReadonlyField` | 只读信息展示框 | 默认 |
| `SearchField` | 带占位搜索或筛选输入 | 默认 |
| `HelperText` | 字段补充说明 | 默认 |
| `InlineErrorText` | 行内错误提示 | 错误 |

#### C. 数据展示类

| 组件名 | 用途 | 主要变体/状态 |
| --- | --- | --- |
| `StatCard` | 顶部数据概览卡片 | 图标+标题+数值 |
| `InfoCard` | 小型信息卡片，如组织编码卡片 | 默认 |
| `TreeList` | 左侧组织树/目录列表 | 默认 |
| `TreeNode` | 树节点 | 收起 / 展开 / 激活 / 带人数徽标 |
| `DataTable` | 标准表格 | 普通表格 / 可选择表格 / 带开关列 |
| `TableToolbar` | 表格上方筛选区域 | 标题 / 筛选 / 统计 |
| `Pagination` | 分页器 | 默认 / 当前页 / 上下页 |
| `StatusTag` | 状态标签 | 成功 / 警告 / 默认 |
| `Switch` | 启用状态切换 | 开 / 关 / 禁用 |
| `Badge` | 小数字或计数提示 | 默认 / 激活 |

#### D. 反馈类

| 组件名 | 用途 | 主要变体/状态 |
| --- | --- | --- |
| `Modal` | 通用弹窗容器 | 表单弹窗 / 列表弹窗 / 宽弹窗 |
| `ConfirmDialog` | 二次确认弹窗 | 默认 / 危险操作 / 离开确认 |
| `Toast` | 全局轻提示 | 错误 / 成功 / 警告 |
| `EmptyState` | 空数据占位 | 图标+标题 |
| `InlineAlert` | 表单区块内提示，如红色说明文字 | 警告 / 错误 |

#### E. 操作类

| 组件名 | 用途 | 主要变体/状态 |
| --- | --- | --- |
| `Button` | 按钮 | 主按钮 / 次按钮 / 危险按钮 / 文本按钮 |
| `IconButton` | 纯图标按钮 | 返回 / 收起 / 关闭 |
| `Checkbox` | 多选 | 未选 / 已选 / 禁用 |
| `Radio` | 单选 | 未选 / 已选 / 禁用 |

### 2.2 业务组件

这些组件是由基础组件组合出来的，建议单独沉淀。

| 组件名 | 组成 | 出现场景 |
| --- | --- | --- |
| `OrgDirectoryPanel` | `SectionHeader + TreeList + TreeNode` | 组织架构、处理组 |
| `GroupMemberTable` | `DataTable + Checkbox + Pagination` | 添加组员、部门负责人设置 |
| `ServiceAccessSummary` | `SectionHeader + StatCard` | 系统列表首页 |
| `ServiceDetailForm` | `Form + ReadonlyField + StatusTag` | 系统详情页 |
| `SdkInterfaceTable` | `DataTable + StatusTag + Switch + Pagination` | 系统详情页接口列表 |
| `SelectionSummaryCard` | 当前对象信息 + 已选人数 | 添加组员、负责人设置 |
| `DangerConfirmDialog` | `ConfirmDialog + DangerButton` | 删除、未保存退出 |

---

## 3. 建议的组件分组结构

如果后面要整理成 Sketch Symbols / 组件库，建议按下面分组：

### 3.1 Foundations

1. Color
2. Typography
3. Radius
4. Shadow
5. Spacing
6. Icon

### 3.2 Layout

1. AppShell
2. Sidebar
3. PageHeader
4. SectionHeader
5. SplitView
6. ContentPanel

### 3.3 Inputs

1. TextInput
2. TextArea
3. Select
4. Checkbox
5. Radio
6. Switch

### 3.4 Data Display

1. StatCard
2. InfoCard
3. TreeNode
4. DataTable
5. Pagination
6. StatusTag
7. Badge

### 3.5 Feedback

1. Toast
2. Modal
3. ConfirmDialog
4. EmptyState
5. InlineAlert

### 3.6 Business

1. OrgDirectoryPanel
2. GroupMemberTable
3. ServiceDetailForm
4. SdkInterfaceTable

---

## 4. 命名建议

建议统一采用：

1. 基础组件用英文名
2. 业务组件用“业务域 + 功能”命名
3. 变体用 `type / state / size` 三类字段控制

示例：

1. `Button / type=primary / state=default`
2. `StatusTag / type=success`
3. `TreeNode / state=active`
4. `Modal / type=form-large`
5. `DataTable / type=selectable`

---

## 5. 从页面里抽出的主要变体

### 5.1 Button

建议至少做 4 种：

1. `primary`
2. `secondary`
3. `danger`
4. `ghost`

### 5.2 StatusTag

从页面中已明确出现：

1. `success`：已接入、已启用
2. `warning`：待接入
3. `default`：普通状态

### 5.3 Modal

建议拆 3 类：

1. `form-modal`
2. `selection-modal`
3. `confirm-modal`

### 5.4 Table

建议拆 3 类：

1. `basic-table`
2. `selectable-table`
3. `switch-table`

### 5.5 TreeNode

建议支持：

1. `default`
2. `expanded`
3. `collapsed`
4. `active`
5. `with-badge`

---

## 6. 设计 Token 初稿

以下为基于 SVG 统计和页面观察整理的建议值。

### 6.1 Color

#### Primary

| Token | 值 | 用途 |
| --- | --- | --- |
| `color-primary-500` | `#0C9B72` | 主色、选中、开关、主操作 |
| `color-primary-400` | `#2FB88D` | 主色浅层级、hover 可参考 |
| `color-primary-100` | `#E8F8F3` | 选中背景、浅提示 |
| `color-primary-050` | `#F3FAF8` | 表头浅底、弱高亮 |

#### Text

| Token | 值 | 用途 |
| --- | --- | --- |
| `color-text-primary` | `#2F2F2F` | 主正文 |
| `color-text-title` | `#222222` | 标题 |
| `color-text-secondary` | `#6F6A62` | 次级说明 |
| `color-text-muted` | `#AAAAAA` | 辅助信息 |
| `color-text-placeholder` | `#CCCCCC` | 占位文本 |

#### Border / Background

| Token | 值 | 用途 |
| --- | --- | --- |
| `color-border-default` | `#E5EAE7` | 输入框、表格边框 |
| `color-border-light` | `#EEEEEE` | 浅分隔线 |
| `color-bg-page` | `#FBFAF8` | 页面底色 |
| `color-bg-surface` | `#FFFFFF` | 卡片、弹窗 |
| `color-bg-soft` | `#FBFDFC` | 柔和区块底色 |

#### Feedback

| Token | 值 | 用途 |
| --- | --- | --- |
| `color-success` | `#0C9B72` | 成功态 |
| `color-success-bg` | `#E0F4EF` | 成功浅底 |
| `color-warning` | `#E07F33` | 警告态 |
| `color-warning-bg` | `#FEF0E5` | 警告浅底 |
| `color-error` | `#E53E3E` | 错误态 |
| `color-error-bg` | `#FAF3F3` | 错误浅底 |

### 6.2 Typography

页面中主要字体：

1. `Source Han Sans SC`
2. `Alibaba PuHuiTi 2.0`

建议沉淀为：

| Token | 值 | 用途 |
| --- | --- | --- |
| `font-family-base` | `Source Han Sans SC` | 全局中文正文 |
| `font-family-number` | `Alibaba PuHuiTi 2.0` | 数字、高亮数据 |

建议字号层级：

| Token | 值 |
| --- | --- |
| `font-size-xs` | `10px` |
| `font-size-sm` | `12px` |
| `font-size-md` | `14px` |
| `font-size-lg` | `16px` |
| `font-size-xl` | `20px` |

### 6.3 Radius

SVG 中高频出现：

| Token | 值 | 用途 |
| --- | --- | --- |
| `radius-sm` | `5px` | 输入框、表格内小控件 |
| `radius-pill` | `12px` | 状态标签 |
| `radius-round` | `15px` | 30x30 圆形图标底 |
| `radius-panel` | 建议补为 `20px` | 主卡片、主弹窗外轮廓 |

### 6.4 Size

页面中可明确抽出的常用尺寸：

| Token | 值 | 用途 |
| --- | --- | --- |
| `control-height-md` | `40px` | 输入框、下拉框 |
| `tag-height` | `20px` | 状态标签 |
| `badge-size` | `20px` | 数量徽标 |
| `avatar-size-sm` | `30px` | 左下角头像卡片 |

---

## 7. 优先落库顺序

建议先做第一批高频组件：

1. `AppShell`
2. `SidebarItem`
3. `PageHeader`
4. `ContentPanel`
5. `FormField`
6. `TextInput`
7. `TextArea`
8. `Select`
9. `Button`
10. `StatusTag`
11. `DataTable`
12. `Pagination`
13. `Modal`
14. `ConfirmDialog`
15. `EmptyState`

第二批再做：

1. `TreeList`
2. `TreeNode`
3. `StatCard`
4. `Switch`
5. `SelectionSummaryCard`
6. `InlineAlert`
7. `Toast`

---

## 8. 页面到组件的映射

### 8.1 系统列表

主要沉淀：

1. `ServiceAccessSummary`
2. `DataTable`
3. `StatusTag`
4. `Modal`
5. `ConfirmDialog`

### 8.2 系统详情页

主要沉淀：

1. `PageHeader`
2. `ServiceDetailForm`
3. `SdkInterfaceTable`
4. `Switch`
5. `ConfirmDialog`

### 8.3 组织架构

主要沉淀：

1. `OrgDirectoryPanel`
2. `TreeNode`
3. `InfoCard`
4. `DataTable`
5. `SelectionModal`

### 8.4 处理组

主要沉淀：

1. `OrgDirectoryPanel`
2. `GroupFormModal`
3. `GroupMemberTable`
4. `EmptyState`
5. `Toast`
6. `DangerConfirmDialog`

---

## 9. 结论

这套稿已经足够整理出一套中后台组件库，核心风格很统一：

1. 左侧固定导航框架
2. 右侧白色大卡片内容区
3. 40px 高表单控件
4. 浅绿色表头和激活态
5. 表格 + 弹窗 + 选择类场景占比很高

如果后面继续往下做，最适合先产出：

1. 一份 Sketch Symbol / Component 结构
2. 一份组件命名规范
3. 一套前端组件清单
