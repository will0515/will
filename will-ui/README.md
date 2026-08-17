# Will UI

将现有 Will 页面里的 `输入框`、`标签`、`Tab`、`步骤` 和通用按钮整合为一套轻量组件库。

## 直接使用

```html
<link rel="stylesheet" href="./dist/will-ui.css">

<script type="module">
  import { initWillUI } from "./dist/will-ui.js";
  initWillUI();
</script>
```

完整组件示例见 `index.html`。

## 组件

| 组件 | 样式类 | 主要变体 |
| --- | --- | --- |
| Button | `.will-button` | `primary`、`secondary`、`danger`、`ghost`、`small` |
| Input | `.will-field` + `.will-input-shell` | `medium`、`small`、`search`、`error`、`disabled`、可清空 |
| Textarea | `.will-textarea-shell` | 默认、错误、禁用、自动增高 |
| Tag | `.will-tag` | `green`、`yellow`、`red`、`blue`、`gray` |
| Tabs | `.will-tabs` | 选中/未选中、数字徽标、键盘操作、动态添加/删除 |
| Steps | `.will-steps` | `complete`、`current`、`pending`、切换、动态添加/删除 |

## 添加与删除

预览页通过声明式按钮管理 Tab 和步骤：

```html
<button data-will-action="add-tab" data-will-target="#my-tabs">添加 Tab</button>
<button data-will-action="remove-tab" data-will-target="#my-tabs">删除当前</button>
```

也可以直接调用 `addTab`、`removeTab`、`addStep`、`removeStep`。

## 事件

交互组件会在容器上触发 `will:change` 事件。

```js
document.addEventListener("will:change", (event) => {
  console.log(event.detail);
});
```

## 自定义主题

在业务入口覆盖 `--will-*` 变量即可：

```css
:root {
  --will-color-primary-500: #0c9b72;
  --will-font-family: "Source Han Sans SC", sans-serif;
}
```
