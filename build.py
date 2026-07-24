from __future__ import annotations

import json
import shutil
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    from markdown import Markdown
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency. Install requirements with `.venv\\Scripts\\python.exe -m pip install -r requirements.txt`."
    ) from exc


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"


def copy_static_assets() -> None:
    ASSETS.mkdir(exist_ok=True)
    for source in (SRC / "static").rglob("*"):
        if not source.is_file():
            continue
        target = ASSETS / source.relative_to(SRC / "static")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def render_markdown(source: Path) -> str:
    md = Markdown(
        extensions=[
            "extra",
            "fenced_code",
            "tables",
            "toc",
            "codehilite",
            "smarty",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "guess_lang": False,
            }
        },
    )
    return md.convert(source.read_text(encoding="utf-8"))


def render_site() -> None:
    data = json.loads((SRC / "content" / "site.json").read_text(encoding="utf-8"))
    env = Environment(
        loader=FileSystemLoader(SRC / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    copy_static_assets()

    template = env.get_template("index.html.j2")
    html = template.render(**data, subtitle=data["home"]["subtitle"], math=False, body_class="home-page")
    (ROOT / "index.html").write_text(html + "\n", encoding="utf-8", newline="\n")

    page_template = env.get_template("page.html.j2")
    for page in data["pages"]:
        content = render_markdown(SRC / "content" / page["source"])
        html = page_template.render(
            **data,
            page=page,
            subtitle=page["subtitle"],
            math=page.get("math", False),
            body_class="inner-page",
            content=content,
        )
        (ROOT / f"{page['slug']}.html").write_text(html + "\n", encoding="utf-8", newline="\n")

    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    render_site()
    print("Generated static pages and assets/ for GitHub Pages.")
