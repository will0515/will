from __future__ import annotations

import re
from pathlib import Path


SOURCE = Path("/Users/edy/Documents/Codex/2026-07-22/ba/outputs/icon-gallery.html")
OUTPUT = Path("/Users/edy/Documents/ssc/outputs/icon-gallery.html")


STYLES = r"""
    /*
      参照 sidebar-navigation.html：
      - 24px 浅色网格画布
      - 半透明白色组件框与柔和阴影
      - 10px 圆角、40px 分类项
      - #0c9b72 品牌绿与 #e0f4ef 选中底色
      - 图标以灰色展示，悬停与选中使用品牌绿
    */

    :root {
      color-scheme: light;
      --canvas: #f1f4f2;
      --surface: #fbfaf8;
      --selected-surface: #e0f4ef;
      --brand: #0c9b72;
      --text-muted: #aaaaaa;
      --icon-muted: #cccccc;
      --ink: #29282d;
      --line: rgba(41, 40, 45, 0.09);
      --shadow: 0 1px 1px rgba(41, 40, 45, 0.04),
        0 18px 50px rgba(41, 40, 45, 0.08);
    }

    * { box-sizing: border-box; }

    html,
    body {
      width: 100%;
      min-height: 100%;
      margin: 0;
    }

    html { scroll-behavior: smooth; }

    body {
      padding: 32px;
      color: var(--ink);
      background:
        linear-gradient(rgba(41, 40, 45, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(41, 40, 45, 0.035) 1px, transparent 1px),
        var(--canvas);
      background-size: 24px 24px;
      font-family: "Source Han Sans SC", "Noto Sans CJK SC", "PingFang SC",
        "Microsoft YaHei", sans-serif;
      line-height: 1.5;
    }

    button,
    input { font: inherit; }

    .app-shell {
      width: min(1480px, 100%);
      min-height: calc(100vh - 64px);
      margin: 0 auto;
      display: grid;
      grid-template-columns: 220px minmax(0, 1fr);
      grid-template-rows: auto 1fr;
      align-items: start;
      overflow: clip;
      border: 1px solid rgba(41, 40, 45, 0.08);
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.72);
      box-shadow: var(--shadow);
    }

    .shell { width: auto; margin: 0; }

    .masthead {
      grid-column: 1 / -1;
      min-height: 96px;
      padding: 22px 26px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      border-bottom: 1px solid var(--line);
      background: rgba(251, 250, 248, 0.72);
      backdrop-filter: blur(18px);
    }

    .eyebrow {
      margin: 0 0 4px;
      color: var(--brand);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.02em;
    }

    h1 {
      margin: 0;
      font-size: 28px;
      font-weight: 650;
      line-height: 36px;
      letter-spacing: -0.03em;
    }

    .summary {
      margin: 0;
      color: rgba(41, 40, 45, 0.54);
      font-size: 13px;
      white-space: nowrap;
    }

    .summary strong {
      color: var(--brand);
      font-weight: 650;
    }

    .toolbar-wrap {
      grid-column: 1;
      grid-row: 2;
      position: sticky;
      top: 16px;
      align-self: start;
      padding: 18px 14px 24px;
      border-right: 1px solid var(--line);
    }

    .toolbar {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .search { position: relative; }

    .search svg {
      position: absolute;
      top: 50%;
      left: 12px;
      width: 18px;
      height: 18px;
      transform: translateY(-50%);
      color: var(--icon-muted);
      pointer-events: none;
    }

    .search input {
      width: 100%;
      height: 40px;
      padding: 0 36px 0 38px;
      border: 1px solid transparent;
      border-radius: 10px;
      outline: none;
      background: var(--surface);
      color: var(--ink);
      font-size: 14px;
      transition:
        border-color 160ms cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 160ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .search input::placeholder { color: var(--text-muted); }

    .search input:focus {
      border-color: var(--brand);
      box-shadow: 0 0 0 3px rgba(12, 155, 114, 0.11);
    }

    .clear-search {
      position: absolute;
      top: 50%;
      right: 5px;
      width: 30px;
      height: 30px;
      border: 0;
      border-radius: 8px;
      transform: translateY(-50%);
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      opacity: 0;
      pointer-events: none;
    }

    .clear-search.is-visible { opacity: 1; pointer-events: auto; }
    .clear-search:hover { color: var(--brand); background: var(--selected-surface); }

    .sidebar-label {
      padding: 0 10px;
      color: rgba(41, 40, 45, 0.42);
      font-size: 12px;
      line-height: 18px;
    }

    .filters {
      display: flex;
      flex-direction: column;
      gap: 0;
    }

    .filter {
      width: 100%;
      height: 40px;
      min-height: 40px;
      padding: 0 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 0;
      border-radius: 10px;
      background: var(--surface);
      color: var(--text-muted);
      cursor: pointer;
      font-size: 14px;
      font-weight: 400;
      text-align: left;
      appearance: none;
      outline: none;
      transition:
        color 160ms cubic-bezier(0.22, 1, 0.36, 1),
        background-color 160ms cubic-bezier(0.22, 1, 0.36, 1),
        transform 120ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .filter span {
      margin: 0;
      color: var(--icon-muted);
      font-size: 11px;
      font-variant-numeric: tabular-nums;
    }

    .filter:hover { color: #7d7d7d; background: var(--canvas); }

    .filter.is-active {
      color: var(--brand);
      background: var(--selected-surface);
      font-weight: 500;
    }

    .filter.is-active span { color: var(--brand); }
    .filter:active { transform: scale(0.985); }

    .filter:focus-visible {
      box-shadow: 0 0 0 2px var(--surface), 0 0 0 4px var(--brand);
    }

    main {
      grid-column: 2;
      grid-row: 2;
      min-width: 0;
      padding: 8px 26px 54px;
    }

    .category-section {
      padding: 26px 0 32px;
      border-bottom: 1px solid var(--line);
    }

    .category-section:last-child { border-bottom: 0; }

    .section-heading {
      display: flex;
      align-items: baseline;
      gap: 9px;
      margin-bottom: 14px;
    }

    .section-heading h2 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      line-height: 24px;
      letter-spacing: -0.01em;
    }

    .section-heading span {
      color: var(--text-muted);
      font-size: 11px;
    }

    .icon-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(126px, 1fr));
      gap: 10px;
    }

    .icon-card {
      min-width: 0;
      padding: 8px 8px 10px;
      border: 1px solid rgba(41, 40, 45, 0.07);
      border-radius: 12px;
      background: var(--surface);
      outline: none;
      cursor: default;
      transition:
        border-color 160ms cubic-bezier(0.22, 1, 0.36, 1),
        background-color 160ms cubic-bezier(0.22, 1, 0.36, 1),
        transform 120ms cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 160ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .icon-card:hover,
    .icon-card:focus-visible {
      border-color: rgba(12, 155, 114, 0.18);
      background: var(--selected-surface);
      box-shadow: 0 8px 22px rgba(41, 40, 45, 0.07);
      transform: translateY(-1px);
    }

    .icon-card:focus-visible {
      box-shadow: 0 0 0 2px var(--surface), 0 0 0 4px var(--brand);
    }

    .icon-stage {
      height: 84px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      background: rgba(241, 244, 242, 0.86);
      transition: background-color 160ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .icon-card:hover .icon-stage,
    .icon-card:focus-visible .icon-stage {
      background: rgba(255, 255, 255, 0.6);
    }

    .icon-mask {
      width: 38px;
      height: 38px;
      display: block;
      background: var(--icon-muted);
      -webkit-mask-image: var(--icon);
      -webkit-mask-repeat: no-repeat;
      -webkit-mask-position: center;
      -webkit-mask-size: contain;
      mask-image: var(--icon);
      mask-repeat: no-repeat;
      mask-position: center;
      mask-size: contain;
      transition:
        background-color 160ms cubic-bezier(0.22, 1, 0.36, 1),
        transform 160ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .icon-card:hover .icon-mask,
    .icon-card:focus-visible .icon-mask {
      background: var(--brand);
      transform: scale(1.04);
    }

    .icon-name {
      margin-top: 8px;
      overflow: hidden;
      color: #77777a;
      font-size: 12px;
      font-weight: 400;
      line-height: 20px;
      text-align: center;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .icon-card:hover .icon-name,
    .icon-card:focus-visible .icon-name { color: var(--brand); }

    .empty {
      display: none;
      min-height: 320px;
      place-items: center;
      color: var(--text-muted);
      text-align: center;
    }

    .empty strong {
      display: block;
      margin-bottom: 6px;
      color: var(--ink);
      font-size: 16px;
      font-weight: 600;
    }

    [hidden] { display: none !important; }

    @media (max-width: 840px) {
      body { padding: 18px; }

      .app-shell {
        min-height: calc(100vh - 36px);
        display: block;
      }

      .masthead {
        min-height: 88px;
        padding: 18px;
      }

      .toolbar-wrap {
        position: sticky;
        z-index: 10;
        top: 0;
        padding: 12px 14px;
        border-right: 0;
        border-bottom: 1px solid var(--line);
        background: rgba(251, 250, 248, 0.9);
        backdrop-filter: blur(18px);
      }

      .toolbar { gap: 10px; }
      .sidebar-label { display: none; }

      .filters {
        flex-direction: row;
        gap: 6px;
        overflow-x: auto;
        scrollbar-width: none;
      }

      .filters::-webkit-scrollbar { display: none; }

      .filter {
        width: auto;
        min-width: max-content;
        padding: 0 13px;
        gap: 8px;
      }

      main { padding: 4px 16px 40px; }
      .icon-grid { grid-template-columns: repeat(auto-fill, minmax(112px, 1fr)); gap: 8px; }
    }

    @media (max-width: 520px) {
      body { padding: 10px; }
      .app-shell { min-height: calc(100vh - 20px); border-radius: 14px; }
      .masthead { align-items: flex-start; flex-direction: column; gap: 6px; }
      h1 { font-size: 24px; line-height: 32px; }
      .icon-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
      }
    }
"""


def restyle(source: str) -> str:
    result = re.sub(
        r"<style>.*?</style>",
        f"<style>{STYLES}\n  </style>",
        source,
        count=1,
        flags=re.DOTALL,
    )
    result = result.replace(
        '<nav class="filters" aria-label="图标分类">',
        '<div class="sidebar-label">分类</div>\n'
        '      <nav class="filters" aria-label="图标分类">',
        1,
    )
    result = result.replace("<body>", '<body>\n  <div class="app-shell">', 1)
    result = result.replace("</body>", "  </div>\n</body>", 1)
    result = re.sub(
        r'<img src="([^"]+)" alt="" width="56" height="56" loading="lazy">',
        lambda match: (
            '<span class="icon-mask" aria-hidden="true" '
            f'style="--icon: url(&quot;{match.group(1)}&quot;)"></span>'
        ),
        result,
    )
    result = result.replace(
        "视觉方向：中性、克制、信息密度适中；深色预览区用于显示原始白色 SVG。",
        "视觉方向：沿用 sidebar-navigation.html 的浅色网格、半透明组件框、品牌绿与选中底色。",
    )
    return result


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    output = restyle(source)
    if output.count('class="icon-mask"') != 445:
        raise RuntimeError("图标替换数量不正确")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
