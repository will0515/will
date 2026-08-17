from __future__ import annotations

import html
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path


SKETCH_FILE = Path("/Users/edy/Desktop/个人组件/icon.sketch")
OUTPUT_FILE = Path("/Users/edy/Documents/ssc/outputs/icon-component.html")
SKETCHTOOL = Path("/Applications/Sketch.app/Contents/MacOS/sketchtool")
PAGE_FILE = "pages/AE747BBC-4BB0-4711-B432-9BAA784D6664.json"


def load_symbols() -> list[dict[str, str]]:
    with zipfile.ZipFile(SKETCH_FILE) as archive:
        page = json.loads(archive.read(PAGE_FILE))

    symbols = []
    for layer in page.get("layers", []):
        if layer.get("_class") != "symbolMaster":
            continue
        full_name = layer.get("name", "icon/未命名")
        parts = [part for part in full_name.split("/") if part]
        category = parts[-2] if len(parts) > 2 else "其他"
        name = parts[-1]
        symbols.append(
            {
                "id": layer["do_objectID"],
                "name": name,
                "category": category,
                "fullName": full_name,
            }
        )
    return symbols


def export_svgs(symbols: list[dict[str, str]]) -> None:
    with tempfile.TemporaryDirectory(prefix="ssc-icon-export-") as temp_dir:
        temp_path = Path(temp_dir)
        for symbol in symbols:
            subprocess.run(
                [
                    str(SKETCHTOOL),
                    "export",
                    "layers",
                    str(SKETCH_FILE),
                    f"--output={temp_path}",
                    "--formats=svg",
                    f"--item={symbol['id']}",
                    "--use-id-for-name=YES",
                    "--overwriting=YES",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            svg = (temp_path / f"{symbol['id']}.svg").read_text(encoding="utf-8")
            symbol["svg"] = svg.replace("\n", "").replace("    ", " ")


def build_html(symbols: list[dict[str, str]]) -> str:
    icon_json = json.dumps(symbols, ensure_ascii=False, separators=(",", ":"))
    category_count = len({item["category"] for item in symbols})
    template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Icon 组件 · __ICON_COUNT__ 个图标</title>
  <style>
    :root {
      color-scheme: light;
      --brand: #0c9b72;
      --brand-soft: #e8f8f3;
      --brand-pale: #f3faf8;
      --page: #f5f6f4;
      --surface: #ffffff;
      --surface-warm: #fbfaf8;
      --text: #2f2f2f;
      --secondary: #6f6a62;
      --muted: #a5aaa7;
      --border: #e5eae7;
      --danger: #e53e3e;
      --shadow: 0 18px 60px rgba(35, 48, 43, 0.08);
      --icon-color: #2f2f2f;
    }

    * { box-sizing: border-box; }
    html, body { width: 100%; min-height: 100%; margin: 0; }
    body {
      color: var(--text);
      background:
        linear-gradient(rgba(47, 47, 47, 0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(47, 47, 47, 0.025) 1px, transparent 1px),
        var(--page);
      background-size: 24px 24px;
      font-family: "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      font-size: 14px;
    }

    button, input, select { font: inherit; }
    button, select, input[type="color"] { cursor: pointer; }
    button:focus-visible, input:focus-visible, select:focus-visible {
      outline: 3px solid rgba(12, 155, 114, 0.16);
      outline-offset: 1px;
    }

    .app {
      width: min(1560px, calc(100% - 40px));
      min-height: calc(100vh - 40px);
      margin: 20px auto;
      position: relative;
      display: grid;
      grid-template-columns: 232px minmax(0, 1fr) 320px;
      grid-template-rows: 76px minmax(0, 1fr);
      overflow: hidden;
      border: 1px solid rgba(47, 47, 47, 0.08);
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.82);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }

    .drop-overlay {
      position: absolute;
      z-index: 45;
      inset: 0;
      display: grid;
      place-items: center;
      border-radius: 18px;
      background: rgba(243, 250, 248, 0.9);
      backdrop-filter: blur(10px);
      opacity: 0;
      pointer-events: none;
      transition: opacity 150ms ease;
    }
    .app.is-dragging .drop-overlay { opacity: 1; }
    .drop-panel {
      width: min(420px, calc(100% - 40px));
      min-height: 220px;
      padding: 36px;
      display: grid;
      place-items: center;
      align-content: center;
      border: 2px dashed var(--brand);
      border-radius: 18px;
      background: rgba(255,255,255,.88);
      color: var(--brand);
      text-align: center;
      box-shadow: var(--shadow);
    }
    .drop-panel svg { width: 42px; height: 42px; margin-bottom: 14px; }
    .drop-panel strong { display: block; color: var(--text); font-size: 18px; }
    .drop-panel span { margin-top: 6px; color: var(--muted); font-size: 12px; }

    .topbar {
      grid-column: 1 / -1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      padding: 0 22px;
      border-bottom: 1px solid var(--border);
      background: rgba(251, 250, 248, 0.82);
    }

    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-mark {
      width: 38px; height: 38px; display: grid; place-items: center;
      border-radius: 12px; background: var(--brand); color: white;
      box-shadow: 0 7px 18px rgba(12, 155, 114, 0.2);
    }
    .brand-mark svg { width: 21px; height: 21px; }
    .brand-copy strong { display: block; font-size: 16px; line-height: 22px; }
    .brand-copy span { color: var(--muted); font-size: 12px; }

    .top-actions { display: flex; align-items: center; gap: 10px; }
    .button {
      height: 40px; padding: 0 15px; display: inline-flex; align-items: center;
      justify-content: center; gap: 7px; border: 1px solid var(--border);
      border-radius: 10px; background: var(--surface); color: var(--text);
      font-weight: 500; transition: 150ms ease;
    }
    .button:hover { border-color: #cbd7d2; background: var(--brand-pale); }
    .button.primary { border-color: var(--brand); background: var(--brand); color: white; }
    .button.primary:hover { background: #087f5d; }
    .button.danger { color: var(--danger); }
    .button svg { width: 18px; height: 18px; }

    .sidebar {
      grid-column: 1; grid-row: 2; min-height: 0; padding: 18px 14px 24px;
      overflow-y: auto; border-right: 1px solid var(--border);
      background: rgba(251, 250, 248, 0.5);
    }

    .search { position: relative; display: block; margin-bottom: 18px; }
    .search svg {
      position: absolute; top: 50%; left: 12px; width: 18px; height: 18px;
      transform: translateY(-50%); color: var(--muted); pointer-events: none;
    }
    .search input {
      width: 100%; height: 40px; padding: 0 34px 0 38px;
      border: 1px solid var(--border); border-radius: 10px;
      background: white; color: var(--text); outline: 0;
    }
    .search input:focus { border-color: var(--brand); }
    .search-clear {
      position: absolute; top: 5px; right: 5px; width: 30px; height: 30px;
      border: 0; border-radius: 8px; background: transparent; color: var(--muted);
    }
    .search-clear:hover { color: var(--brand); background: var(--brand-soft); }

    .side-label { margin: 0 10px 8px; color: var(--muted); font-size: 12px; }
    .categories { display: grid; gap: 2px; }
    .category {
      width: 100%; height: 40px; padding: 0 10px; display: flex; align-items: center;
      justify-content: space-between; border: 0; border-radius: 10px;
      background: transparent; color: var(--secondary); text-align: left;
    }
    .category:hover { background: #f0f3f1; color: var(--text); }
    .category.active { background: var(--brand-soft); color: var(--brand); font-weight: 600; }
    .category span { color: var(--muted); font-size: 11px; }
    .category.active span { color: var(--brand); }

    .content {
      grid-column: 2; grid-row: 2; min-width: 0; min-height: 0;
      padding: 24px 26px 44px; overflow-y: auto; background: rgba(255,255,255,0.42);
    }
    .content-header {
      display: flex; align-items: flex-end; justify-content: space-between;
      gap: 20px; margin-bottom: 20px;
    }
    .content-header h1 { margin: 0; font-size: 24px; line-height: 34px; letter-spacing: -0.03em; }
    .content-header p { margin: 4px 0 0; color: var(--muted); font-size: 13px; }
    .quick-color { display: flex; align-items: center; gap: 8px; }
    .quick-color-label { margin-right: 2px; color: var(--muted); font-size: 12px; }
    .swatch {
      width: 28px; height: 28px; border: 3px solid white; border-radius: 50%;
      background: var(--swatch); box-shadow: 0 0 0 1px var(--border); padding: 0;
    }
    .swatch.active { box-shadow: 0 0 0 2px var(--brand); }

    .icon-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(116px, 1fr));
      gap: 10px;
    }
    .icon-card {
      position: relative; min-width: 0; padding: 9px 9px 10px;
      border: 1px solid var(--border); border-radius: 12px; background: var(--surface);
      transition: 150ms ease; user-select: none;
    }
    .icon-card:hover { border-color: rgba(12,155,114,.35); transform: translateY(-1px); box-shadow: 0 8px 20px rgba(35,48,43,.07); }
    .icon-card.selected { border-color: var(--brand); background: var(--brand-pale); box-shadow: 0 0 0 2px rgba(12,155,114,.1); }
    .icon-card button.card-main {
      width: 100%; padding: 0; border: 0; background: transparent; color: inherit; text-align: inherit;
    }
    .icon-stage {
      height: 76px; display: grid; place-items: center; border-radius: 8px;
      background: #f4f6f5;
    }
    .icon-mask {
      width: 34px; height: 34px; display: block; background: var(--icon-color);
      -webkit-mask: var(--src) center / contain no-repeat;
      mask: var(--src) center / contain no-repeat;
      transition: 150ms ease;
    }
    .icon-card:hover .icon-mask, .icon-card.selected .icon-mask { background: var(--brand); transform: scale(1.05); }
    .icon-name { margin-top: 8px; overflow: hidden; color: var(--secondary); font-size: 12px; line-height: 20px; text-align: center; text-overflow: ellipsis; white-space: nowrap; }
    .upload-badge {
      position: absolute; top: 14px; right: 14px; height: 18px; padding: 0 5px;
      display: inline-flex; align-items: center; border-radius: 9px;
      background: var(--brand-soft); color: var(--brand); font-size: 10px;
    }

    .empty { display: none; min-height: 360px; place-items: center; text-align: center; color: var(--muted); }
    .empty svg { width: 48px; height: 48px; margin-bottom: 12px; color: #cbd2ce; }
    .empty strong { display: block; margin-bottom: 4px; color: var(--text); font-size: 16px; }

    .inspector {
      grid-column: 3; grid-row: 2; min-height: 0; padding: 22px;
      overflow-y: auto; border-left: 1px solid var(--border); background: var(--surface-warm);
    }
    .inspector-title { margin: 0 0 16px; font-size: 15px; }
    .preview {
      height: 190px; display: grid; place-items: center; margin-bottom: 18px;
      border: 1px solid var(--border); border-radius: 14px;
      background:
        linear-gradient(45deg, #f0f2f1 25%, transparent 25%),
        linear-gradient(-45deg, #f0f2f1 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #f0f2f1 75%),
        linear-gradient(-45deg, transparent 75%, #f0f2f1 75%), white;
      background-size: 16px 16px; background-position: 0 0,0 8px,8px -8px,-8px 0;
    }
    .preview-mask {
      width: 104px; height: 104px; display: block; background: var(--icon-color);
      -webkit-mask: var(--src) center / contain no-repeat;
      mask: var(--src) center / contain no-repeat;
    }
    .selected-meta { margin-bottom: 18px; }
    .selected-meta strong { display: block; overflow: hidden; font-size: 16px; line-height: 24px; text-overflow: ellipsis; white-space: nowrap; }
    .selected-meta span { color: var(--muted); font-size: 12px; }
    .field { margin-bottom: 15px; }
    .field > label { display: block; margin-bottom: 7px; color: var(--secondary); font-size: 12px; }
    .color-row { display: grid; grid-template-columns: 40px 1fr; gap: 8px; }
    .color-picker { width: 40px; height: 40px; padding: 3px; border: 1px solid var(--border); border-radius: 10px; background: white; }
    .control {
      width: 100%; height: 40px; padding: 0 11px; border: 1px solid var(--border);
      border-radius: 10px; outline: 0; background: white; color: var(--text);
    }
    .control:focus { border-color: var(--brand); }
    .field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .category-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 8px; }
    .category-row .button { min-width: 68px; padding: 0 12px; }
    .download-button { width: 100%; margin-top: 4px; }
    .inspector-empty { height: calc(100% - 40px); display: grid; place-items: center; color: var(--muted); text-align: center; }
    .inspector-empty svg { width: 42px; height: 42px; margin-bottom: 10px; color: #cbd2ce; }
    .inspector-empty p { margin: 0; line-height: 22px; }
    .remove-wrap { margin-top: 12px; }

    .toast {
      position: fixed; left: 50%; bottom: 28px; z-index: 50; padding: 11px 16px;
      border-radius: 10px; background: #29312e; color: white; box-shadow: var(--shadow);
      transform: translate(-50%, 18px); opacity: 0; pointer-events: none;
      transition: 180ms ease;
    }
    .toast.show { transform: translate(-50%, 0); opacity: 1; }
    .toast.error { background: #a93232; }
    #file-input { position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none; }
    [hidden] { display: none !important; }

    @media (max-width: 1120px) {
      .app { grid-template-columns: 210px minmax(0,1fr); }
      .inspector {
        position: fixed; z-index: 30; top: 0; right: 0; width: 320px; height: 100vh;
        transform: translateX(100%); box-shadow: -16px 0 50px rgba(35,48,43,.12); transition: 180ms ease;
      }
      .inspector.open { transform: translateX(0); }
    }
    @media (max-width: 760px) {
      .app { width: 100%; min-height: 100vh; margin: 0; grid-template-columns: 1fr; grid-template-rows: auto auto 1fr; border: 0; border-radius: 0; }
      .topbar { grid-column: 1; grid-row: 1; padding: 14px 16px; }
      .brand-copy span { display: none; }
      .sidebar { grid-column: 1; grid-row: 2; padding: 12px 14px; overflow: visible; border-right: 0; border-bottom: 1px solid var(--border); }
      .search { margin-bottom: 10px; }
      .side-label { display: none; }
      .categories { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; }
      .category { min-width: max-content; padding: 0 13px; gap: 8px; }
      .content { grid-column: 1; grid-row: 3; padding: 20px 16px 40px; }
      .content-header { align-items: flex-start; flex-direction: column; }
      .icon-grid { grid-template-columns: repeat(3, minmax(0,1fr)); }
      .top-actions .button:first-of-type { display: none; }
    }
    @media (max-width: 430px) {
      .icon-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
      .inspector { width: min(320px, 92vw); }
    }
    @media (prefers-reduced-motion: reduce) { * { transition-duration: .01ms !important; } }
  </style>
</head>
<body>
  <div class="app" id="app-root">
    <div class="drop-overlay" id="drop-overlay" aria-hidden="true">
      <div class="drop-panel">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <strong>松开以上传图标</strong>
        <span>支持 SVG、PNG、JPG、WebP，可同时拖入多个文件</span>
      </div>
    </div>
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M4 6.2C4 5 5 4 6.2 4h11.6C19 4 20 5 20 6.2v11.6C20 19 19 20 17.8 20H6.2C5 20 4 19 4 17.8V6.2Z" stroke="currentColor" stroke-width="2"/><path d="M8 12h8M12 8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div class="brand-copy"><strong>Icon 组件</strong><span>统一管理、调整与导出图标资产</span></div>
      </div>
      <div class="top-actions">
        <button class="button" id="reset-color" type="button">恢复默认色</button>
        <button class="button primary" id="upload-button" type="button"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>上传图标</button>
        <input id="file-input" type="file" accept=".svg,image/svg+xml,image/png,image/jpeg,image/webp" multiple>
      </div>
    </header>

    <aside class="sidebar">
      <label class="search">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="m16.5 16.5 4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <input id="search-input" type="search" placeholder="搜索图标" autocomplete="off" aria-label="搜索图标">
        <button class="search-clear" id="search-clear" type="button" aria-label="清空搜索">×</button>
      </label>
      <p class="side-label">分类</p>
      <nav class="categories" id="categories" aria-label="图标分类"></nav>
    </aside>

    <main class="content">
      <div class="content-header">
        <div><h1 id="page-title">全部图标</h1><p><span id="visible-count">__ICON_COUNT__</span> 个图标 · 来自 icon.sketch</p></div>
        <div class="quick-color" aria-label="快捷颜色">
          <span class="quick-color-label">颜色</span>
          <button class="swatch active" type="button" style="--swatch:#2f2f2f" data-color="#2F2F2F" aria-label="深灰色"></button>
          <button class="swatch" type="button" style="--swatch:#0c9b72" data-color="#0C9B72" aria-label="品牌绿色"></button>
          <button class="swatch" type="button" style="--swatch:#2563eb" data-color="#2563EB" aria-label="蓝色"></button>
          <button class="swatch" type="button" style="--swatch:#e53e3e" data-color="#E53E3E" aria-label="红色"></button>
        </div>
      </div>
      <div class="icon-grid" id="icon-grid"></div>
      <div class="empty" id="empty-state"><div><svg viewBox="0 0 24 24" fill="none"><path d="M4 6.2C4 5 5 4 6.2 4h11.6C19 4 20 5 20 6.2v11.6C20 19 19 20 17.8 20H6.2C5 20 4 19 4 17.8V6.2Z" stroke="currentColor" stroke-width="1.7"/><path d="m8 15 2.3-2.3a1 1 0 0 1 1.4 0L14 15l1.3-1.3a1 1 0 0 1 1.4 0L19 16M15.5 9.5h.01" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg><strong>没有找到匹配图标</strong><span>试试其他关键词或分类</span></div></div>
    </main>

    <aside class="inspector" id="inspector" aria-label="图标设置">
      <h2 class="inspector-title">图标设置</h2>
      <div class="inspector-empty" id="inspector-empty"><div><svg viewBox="0 0 24 24" fill="none"><path d="M4 6.2C4 5 5 4 6.2 4h11.6C19 4 20 5 20 6.2v11.6C20 19 19 20 17.8 20H6.2C5 20 4 19 4 17.8V6.2Z" stroke="currentColor" stroke-width="1.7"/><path d="M8 12h8M12 8v8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg><p>选择一个图标<br>即可修改颜色并下载</p></div></div>
      <div id="inspector-form" hidden>
        <div class="preview"><span class="preview-mask" id="preview-mask"></span></div>
        <div class="selected-meta"><strong id="selected-name"></strong><span id="selected-category"></span></div>
        <div class="field">
          <label for="category-input">所属分类</label>
          <div class="category-row">
            <input class="control" id="category-input" list="category-options" maxlength="24" placeholder="选择或输入分类">
            <button class="button" id="save-category" type="button">应用</button>
          </div>
          <datalist id="category-options"></datalist>
        </div>
        <div class="field"><label for="color-picker">图标颜色</label><div class="color-row"><input class="color-picker" id="color-picker" type="color" value="#2f2f2f"><input class="control" id="color-text" value="#2F2F2F" maxlength="7" aria-label="颜色十六进制值"></div></div>
        <div class="field-row">
          <div class="field"><label for="format-select">文件格式</label><select class="control" id="format-select"><option value="svg">SVG</option><option value="png">PNG</option><option value="webp">WebP</option><option value="jpg">JPG</option></select></div>
          <div class="field"><label for="size-select">导出尺寸</label><select class="control" id="size-select"><option value="24">24 × 24</option><option value="32">32 × 32</option><option value="48">48 × 48</option><option value="64" selected>64 × 64</option><option value="128">128 × 128</option><option value="256">256 × 256</option></select></div>
        </div>
        <button class="button primary download-button" id="download-button" type="button"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 4v12m0 0 4.5-4.5M12 16l-4.5-4.5M5 20h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>下载图标</button>
        <div class="remove-wrap" id="remove-wrap"><button class="button danger download-button" id="remove-button" type="button">删除图标</button></div>
      </div>
    </aside>
  </div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <script>
    const BUILT_IN_ICONS = __ICON_DATA__;
    const DELETED_STORAGE_KEY = 'ssc-icon-manager-deleted';
    const CATEGORY_STORAGE_KEY = 'ssc-icon-manager-categories';
    function loadDeletedIds() {
      try {
        const value = JSON.parse(localStorage.getItem(DELETED_STORAGE_KEY) || '[]');
        return new Set(Array.isArray(value) ? value : []);
      } catch {
        return new Set();
      }
    }
    function loadCategoryOverrides() {
      try {
        const value = JSON.parse(localStorage.getItem(CATEGORY_STORAGE_KEY) || '{}');
        return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
      } catch {
        return {};
      }
    }
    const state = {
      icons: [],
      category: '全部',
      query: '',
      color: '#2F2F2F',
      selectedId: null,
      deletedIds: loadDeletedIds(),
      categoryOverrides: loadCategoryOverrides()
    };
    const els = {
      grid: document.getElementById('icon-grid'), categories: document.getElementById('categories'),
      search: document.getElementById('search-input'), searchClear: document.getElementById('search-clear'),
      count: document.getElementById('visible-count'), title: document.getElementById('page-title'),
      empty: document.getElementById('empty-state'), inspector: document.getElementById('inspector'),
      inspectorEmpty: document.getElementById('inspector-empty'), inspectorForm: document.getElementById('inspector-form'),
      preview: document.getElementById('preview-mask'), selectedName: document.getElementById('selected-name'),
      selectedCategory: document.getElementById('selected-category'), colorPicker: document.getElementById('color-picker'),
      colorText: document.getElementById('color-text'), format: document.getElementById('format-select'),
      size: document.getElementById('size-select'), download: document.getElementById('download-button'),
      upload: document.getElementById('upload-button'), fileInput: document.getElementById('file-input'),
      resetColor: document.getElementById('reset-color'), toast: document.getElementById('toast'),
      removeWrap: document.getElementById('remove-wrap'), remove: document.getElementById('remove-button'),
      app: document.getElementById('app-root'), categoryInput: document.getElementById('category-input'),
      categoryOptions: document.getElementById('category-options'), saveCategory: document.getElementById('save-category')
    };

    const toDataUrl = (svg) => `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    const normalizeIcons = () => BUILT_IN_ICONS
      .filter(icon => !state.deletedIds.has(icon.id))
      .map(icon => {
        const category = state.categoryOverrides[icon.id] || icon.category;
        return {
          ...icon,
          category,
          fullName: `icon/${category}/${icon.name}`,
          src: toDataUrl(icon.svg),
          uploaded: false,
          mime: 'image/svg+xml'
        };
      });
    state.icons = normalizeIcons();

    function showToast(message, error = false) {
      els.toast.textContent = message;
      els.toast.classList.toggle('error', error);
      els.toast.classList.add('show');
      clearTimeout(showToast.timer);
      showToast.timer = setTimeout(() => els.toast.classList.remove('show'), 1800);
    }

    function categoryCounts() {
      return state.icons.reduce((map, icon) => map.set(icon.category, (map.get(icon.category) || 0) + 1), new Map());
    }

    function renderCategories() {
      const counts = categoryCounts();
      const preferred = ['箭头', '业务', '交互', '图表', '界面', '编辑', '文件', '导航', '系统', '用户', '上传'];
      const names = [...counts.keys()].sort((a, b) => {
        const ai = preferred.indexOf(a), bi = preferred.indexOf(b);
        if (ai === -1 && bi === -1) return a.localeCompare(b, 'zh-CN');
        if (ai === -1) return 1; if (bi === -1) return -1; return ai - bi;
      });
      els.categories.innerHTML = [{ name: '全部', count: state.icons.length }, ...names.map(name => ({ name, count: counts.get(name) }))]
        .map(item => `<button class="category ${state.category === item.name ? 'active' : ''}" type="button" data-category="${escapeHtml(item.name)}"><span class="category-name">${escapeHtml(item.name)}</span><span>${item.count}</span></button>`).join('');
      els.categories.querySelectorAll('.category').forEach(button => button.addEventListener('click', () => {
        state.category = button.dataset.category; renderCategories(); renderGrid();
      }));
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>'"]/g, char => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', "'":'&#39;', '"':'&quot;' }[char]));
    }

    function filteredIcons() {
      const query = state.query.trim().toLocaleLowerCase('zh-CN');
      return state.icons.filter(icon => (state.category === '全部' || icon.category === state.category) && (!query || `${icon.name} ${icon.fullName}`.toLocaleLowerCase('zh-CN').includes(query)));
    }

    function renderGrid() {
      const icons = filteredIcons();
      document.documentElement.style.setProperty('--icon-color', state.color);
      els.count.textContent = String(icons.length);
      els.title.textContent = state.category === '全部' ? '全部图标' : `${state.category}图标`;
      els.empty.style.display = icons.length ? 'none' : 'grid';
      els.grid.innerHTML = icons.map(icon => `<article class="icon-card ${icon.id === state.selectedId ? 'selected' : ''}" data-id="${escapeHtml(icon.id)}"><button class="card-main" type="button" aria-label="选择${escapeHtml(icon.name)}图标"><div class="icon-stage"><span class="icon-mask" style="--src:url('${icon.src}')"></span></div><div class="icon-name" title="${escapeHtml(icon.fullName)}">${escapeHtml(icon.name)}</div></button>${icon.uploaded ? '<span class="upload-badge">上传</span>' : ''}</article>`).join('');
      els.grid.querySelectorAll('.icon-card').forEach(card => {
        card.querySelector('.card-main').addEventListener('click', () => selectIcon(card.dataset.id));
        card.querySelector('.card-main').addEventListener('dblclick', () => { selectIcon(card.dataset.id); downloadSelected(); });
      });
    }

    function selectedIcon() { return state.icons.find(icon => icon.id === state.selectedId) || null; }

    function renderCategoryOptions() {
      const categories = [...new Set(state.icons.map(icon => icon.category))]
        .filter(category => category && category !== '全部')
        .sort((a, b) => a.localeCompare(b, 'zh-CN'));
      els.categoryOptions.innerHTML = categories
        .map(category => `<option value="${escapeHtml(category)}"></option>`)
        .join('');
    }

    function selectIcon(id) {
      state.selectedId = id;
      const icon = selectedIcon();
      if (!icon) return;
      els.inspectorEmpty.hidden = true;
      els.inspectorForm.hidden = false;
      els.preview.style.setProperty('--src', `url('${icon.src}')`);
      els.selectedName.textContent = icon.name;
      els.selectedCategory.textContent = icon.fullName;
      renderCategoryOptions();
      els.categoryInput.value = icon.category;
      els.removeWrap.style.display = 'block';
      els.inspector.classList.add('open');
      renderGrid();
    }

    function setColor(value) {
      const normalized = value.startsWith('#') ? value.toUpperCase() : `#${value.toUpperCase()}`;
      if (!/^#[0-9A-F]{6}$/.test(normalized)) return false;
      state.color = normalized;
      els.colorPicker.value = normalized.toLowerCase();
      els.colorText.value = normalized;
      document.documentElement.style.setProperty('--icon-color', normalized);
      document.querySelectorAll('.swatch').forEach(item => item.classList.toggle('active', item.dataset.color.toUpperCase() === normalized));
      return true;
    }

    function coloredSvg(svg, color, size) {
      const doc = new DOMParser().parseFromString(svg, 'image/svg+xml');
      const root = doc.documentElement;
      if (root.nodeName.toLowerCase() !== 'svg') throw new Error('SVG 文件无效');
      const originalWidth = Number.parseFloat(root.getAttribute('width')) || 24;
      const originalHeight = Number.parseFloat(root.getAttribute('height')) || 24;
      if (!root.hasAttribute('viewBox')) root.setAttribute('viewBox', `0 0 ${originalWidth} ${originalHeight}`);
      root.setAttribute('width', size); root.setAttribute('height', size);
      root.setAttribute('color', color);
      [...root.querySelectorAll('*'), root].forEach(node => {
        ['fill', 'stroke'].forEach(attr => {
          const value = node.getAttribute(attr);
          if (value && value !== 'none' && !value.startsWith('url(')) node.setAttribute(attr, color);
        });
        const style = node.getAttribute('style');
        if (style) node.setAttribute('style', style.replace(/(fill|stroke)\s*:\s*(?!none|url\()[^;]+/gi, `$1:${color}`));
      });
      if (!root.hasAttribute('fill')) root.setAttribute('fill', color);
      root.querySelectorAll('title').forEach(title => title.remove());
      return new XMLSerializer().serializeToString(root);
    }

    function rasterAsSvg(icon, color, size) {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"><defs><mask id="icon-mask"><image href="${icon.src}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet"/></mask></defs><rect width="${size}" height="${size}" fill="${color}" mask="url(#icon-mask)"/></svg>`;
    }

    function loadImage(src) {
      return new Promise((resolve, reject) => { const image = new Image(); image.onload = () => resolve(image); image.onerror = reject; image.src = src; });
    }

    async function rasterBlob(icon, type, size, color) {
      const source = icon.svg ? toDataUrl(coloredSvg(icon.svg, color, size)) : icon.src;
      const image = await loadImage(source);
      const canvas = document.createElement('canvas'); canvas.width = size; canvas.height = size;
      const context = canvas.getContext('2d');
      const iconCanvas = document.createElement('canvas'); iconCanvas.width = size; iconCanvas.height = size;
      const iconContext = iconCanvas.getContext('2d');
      const scale = Math.min(size / image.width, size / image.height);
      const width = image.width * scale, height = image.height * scale;
      const x = (size - width) / 2, y = (size - height) / 2;
      iconContext.drawImage(image, x, y, width, height);
      if (!icon.svg) { iconContext.globalCompositeOperation = 'source-in'; iconContext.fillStyle = color; iconContext.fillRect(0, 0, size, size); }
      if (type === 'image/jpeg') { context.fillStyle = '#FFFFFF'; context.fillRect(0, 0, size, size); }
      context.drawImage(iconCanvas, 0, 0);
      return new Promise(resolve => canvas.toBlob(resolve, type, .96));
    }

    function saveBlob(blob, filename) {
      const url = URL.createObjectURL(blob); const anchor = document.createElement('a');
      anchor.href = url; anchor.download = filename; document.body.appendChild(anchor); anchor.click(); anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    async function downloadSelected() {
      const icon = selectedIcon(); if (!icon) { showToast('请先选择一个图标', true); return; }
      const format = els.format.value; const size = Number(els.size.value); const safeName = icon.name.replace(/[\\/:*?"<>|]/g, '-');
      try {
        if (format === 'svg') {
          const svg = icon.svg ? coloredSvg(icon.svg, state.color, size) : rasterAsSvg(icon, state.color, size);
          saveBlob(new Blob([svg], { type: 'image/svg+xml;charset=utf-8' }), `${safeName}.svg`);
        } else {
          const mime = format === 'jpg' ? 'image/jpeg' : `image/${format}`;
          const blob = await rasterBlob(icon, mime, size, state.color);
          if (!blob) throw new Error('当前浏览器不支持该格式');
          saveBlob(blob, `${safeName}.${format}`);
        }
        showToast(`已下载 ${safeName}.${format}`);
      } catch (error) { showToast(error.message || '下载失败', true); }
    }

    function readFile(file) {
      return new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = reject; reader.readAsDataURL(file); });
    }
    function readText(file) {
      return new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = reject; reader.readAsText(file); });
    }

    async function uploadFiles(files) {
      const accepted = [...files].filter(file => /svg|png|jpe?g|webp/i.test(file.type) || /\.(svg|png|jpe?g|webp)$/i.test(file.name));
      if (!accepted.length) { showToast('请选择 SVG、PNG、JPG 或 WebP 文件', true); return; }
      for (const file of accepted) {
        const isSvg = file.type.includes('svg') || file.name.toLowerCase().endsWith('.svg');
        const name = file.name.replace(/\.[^.]+$/, '');
        const icon = { id: `upload-${Date.now()}-${Math.random().toString(16).slice(2)}`, name, category: '上传', fullName: `上传/${name}`, uploaded: true, mime: file.type || (isSvg ? 'image/svg+xml' : 'image/png') };
        if (isSvg) { icon.svg = await readText(file); icon.src = toDataUrl(icon.svg); }
        else { icon.src = await readFile(file); }
        state.icons.unshift(icon); state.selectedId = icon.id;
      }
      state.category = '上传'; renderCategories(); renderGrid(); selectIcon(state.selectedId);
      showToast(`已上传 ${accepted.length} 个图标`);
      els.fileInput.value = '';
    }

    els.search.addEventListener('input', () => { state.query = els.search.value; renderGrid(); });
    els.searchClear.addEventListener('click', () => { els.search.value = ''; state.query = ''; els.search.focus(); renderGrid(); });
    els.upload.addEventListener('click', () => els.fileInput.click());
    els.fileInput.addEventListener('change', () => uploadFiles(els.fileInput.files));
    let dragDepth = 0;
    const draggingFiles = event => Array.from(event.dataTransfer?.types || []).includes('Files');
    document.addEventListener('dragenter', event => {
      if (!draggingFiles(event)) return;
      event.preventDefault();
      dragDepth += 1;
      els.app.classList.add('is-dragging');
    });
    document.addEventListener('dragover', event => {
      if (!draggingFiles(event)) return;
      event.preventDefault();
      if (event.dataTransfer) event.dataTransfer.dropEffect = 'copy';
    });
    document.addEventListener('dragleave', event => {
      if (!draggingFiles(event)) return;
      dragDepth = Math.max(0, dragDepth - 1);
      if (dragDepth === 0) els.app.classList.remove('is-dragging');
    });
    document.addEventListener('drop', event => {
      if (!draggingFiles(event)) return;
      event.preventDefault();
      dragDepth = 0;
      els.app.classList.remove('is-dragging');
      if (event.dataTransfer?.files?.length) uploadFiles(event.dataTransfer.files);
    });
    els.download.addEventListener('click', downloadSelected);
    els.saveCategory.addEventListener('click', () => {
      const icon = selectedIcon(); if (!icon) return;
      const nextCategory = els.categoryInput.value.trim();
      if (!nextCategory) { showToast('请输入分类名称', true); els.categoryInput.focus(); return; }
      if (nextCategory === '全部') { showToast('“全部”不能作为分类名称', true); els.categoryInput.focus(); return; }
      icon.category = nextCategory;
      icon.fullName = icon.uploaded ? `${nextCategory}/${icon.name}` : `icon/${nextCategory}/${icon.name}`;
      if (!icon.uploaded) {
        state.categoryOverrides[icon.id] = nextCategory;
        localStorage.setItem(CATEGORY_STORAGE_KEY, JSON.stringify(state.categoryOverrides));
      }
      state.category = nextCategory;
      renderCategories(); renderGrid(); selectIcon(icon.id);
      showToast(`已调整到“${nextCategory}”分类`);
    });
    els.categoryInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') els.saveCategory.click();
    });
    els.colorPicker.addEventListener('input', () => setColor(els.colorPicker.value));
    els.colorText.addEventListener('change', () => { if (!setColor(els.colorText.value)) { els.colorText.value = state.color; showToast('请输入 6 位十六进制颜色', true); } });
    els.resetColor.addEventListener('click', () => { setColor('#2F2F2F'); showToast('已恢复默认颜色'); });
    document.querySelectorAll('.swatch').forEach(button => button.addEventListener('click', () => setColor(button.dataset.color)));
    els.remove.addEventListener('click', () => {
      const icon = selectedIcon(); if (!icon) return;
      if (!window.confirm(`确定删除“${icon.name}”图标吗？`)) return;
      if (!icon.uploaded) {
        state.deletedIds.add(icon.id);
        localStorage.setItem(DELETED_STORAGE_KEY, JSON.stringify([...state.deletedIds]));
      }
      state.icons = state.icons.filter(item => item.id !== icon.id); state.selectedId = null;
      els.inspectorForm.hidden = true; els.inspectorEmpty.hidden = false; els.inspector.classList.remove('open');
      if (state.category !== '全部' && !state.icons.some(item => item.category === state.category)) state.category = '全部';
      renderCategories(); renderGrid(); showToast(`已删除 ${icon.name}`);
    });
    document.addEventListener('keydown', event => {
      if ((event.key === 'd' || event.key === 'D') && !/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)) downloadSelected();
      if (event.key === 'Escape') els.inspector.classList.remove('open');
    });

    renderCategories(); renderGrid();
  </script>
</body>
</html>'''
    return (
        template.replace("__ICON_COUNT__", str(len(symbols)))
        .replace("__CATEGORY_COUNT__", str(category_count))
        .replace("__ICON_DATA__", icon_json)
    )


def main() -> None:
    symbols = load_symbols()
    export_svgs(symbols)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(build_html(symbols), encoding="utf-8")
    print(f"Built {OUTPUT_FILE} with {len(symbols)} icons")


if __name__ == "__main__":
    main()
