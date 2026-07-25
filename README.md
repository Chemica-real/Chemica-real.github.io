# Chemica-real.github.io

这是 Chemica_ 的 GitHub Pages 喵窝主页。站点使用 Python + Jinja2 在本地生成静态 HTML，没有在线后端。

## 本地生成

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe build.py
```

生成结果会写入仓库根目录的 `index.html`、各栏目页面和 `assets/`，可以直接由 GitHub Pages 从分支根目录发布。

## 修改内容

- 全站导航、底部、主页内容、页面列表：`src/content/site.json`
- 笔记：`src/content/notes/`
- 文学类：`src/content/literature/`
- 想法和喵叫：`src/content/thoughts/`
- 其他：`src/content/others/`
- 美图页面正文：`src/content/pages/gallery.md`
- HTML 模板：`src/templates/`
- 样式：`src/static/styles.css`
- 导航和音乐控件：`src/static/nav.js`

## 栏目规则

在 `notes`、`literature`、`thoughts`、`others` 四个文件夹里可以直接放 `.md` 文件，也可以继续创建嵌套文件夹。

构建时会自动生成：

- 栏目列表页：先显示文件夹，再显示 Markdown 文件
- 排序规则：文件夹按名称降序，Markdown 文件也按名称降序
- 文章详情页：每个 Markdown 文件生成一个独立页面
- 详情页底部：上一篇/下一篇玻璃态按钮，首尾不存在时显示灰色不可点状态

## 内容能力

- Markdown 页面
- LaTeX 公式，笔记页默认启用 MathJax
- Python、C++ 等代码块高亮
- 每个页面都有统一的顶部引导栏和底部区域
