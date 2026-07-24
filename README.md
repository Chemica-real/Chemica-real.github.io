# Chemica-real.github.io

这是 Chemica_的 GitHub Pages 喵窝主页。站点使用 Python + Jinja2 在本地生成静态 HTML，没有在线后端。

## 本地生成

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe build.py
```

生成结果会写入仓库根目录的 `index.html` 和 `assets/`，可以直接由 GitHub Pages 从分支根目录发布。

## 修改内容

- 全站导航、底部、主页内容、页面列表：`src/content/site.json`
- 笔记、文学、想法、美图、其他页面正文：`src/content/pages/`
- HTML 模板：`src/templates/`
- 样式：`src/static/styles.css`
- 自动隐藏导航：`src/static/nav.js`

## 内容能力

- Markdown 页面
- LaTeX 公式，笔记页默认启用 MathJax
- Python、C++ 等代码块高亮
- 每个页面都有统一的顶部引导栏和底部区域
