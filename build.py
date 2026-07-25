from __future__ import annotations

import json
import os
import shutil
import hashlib
from pathlib import Path
from urllib.parse import quote

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
MANAGED_SECTIONS = {"notes", "literature", "thoughts", "others"}


def copy_static_assets() -> None:
    ASSETS.mkdir(exist_ok=True)
    for source in (SRC / "static").rglob("*"):
        if not source.is_file():
            continue
        target = ASSETS / source.relative_to(SRC / "static")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def static_asset_version() -> str:
    digest = hashlib.sha1()
    for relative in (Path("styles.css"), Path("nav.js")):
        path = SRC / "static" / relative
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()[:10]


def remove_managed_outputs() -> None:
    for slug in MANAGED_SECTIONS:
        output_dir = (ROOT / slug).resolve()
        if output_dir.exists():
            output_dir.relative_to(ROOT.resolve())
            shutil.rmtree(output_dir)


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


def url_path(path: Path) -> str:
    return "/".join(quote(part) for part in path.parts)


def relative_url(from_file: Path, target_file: Path) -> str:
    relative = Path(os.path.relpath(target_file, from_file.parent))
    return url_path(relative)


def asset_prefix(output_file: Path) -> str:
    relative = Path(os.path.relpath(ROOT, output_file.parent))
    if str(relative) == ".":
        return ""
    return url_path(relative) + "/"


def output_for_markdown(section_slug: str, section_root: Path, source: Path) -> Path:
    relative = source.relative_to(section_root).with_suffix(".html")
    return ROOT / section_slug / relative


def output_for_folder(section_slug: str, section_root: Path, folder: Path) -> Path:
    relative = folder.relative_to(section_root)
    if str(relative) == ".":
        return ROOT / f"{section_slug}.html"
    return ROOT / section_slug / relative / "index.html"


def sorted_children(folder: Path) -> tuple[list[Path], list[Path]]:
    children = [child for child in folder.iterdir() if not child.name.startswith(".")]
    folders = sorted((child for child in children if child.is_dir()), key=lambda p: p.name.lower())
    markdown_files = sorted((child for child in children if child.suffix.lower() == ".md"), key=lambda p: p.name.lower())
    return folders, markdown_files


def collect_documents(folder: Path) -> list[Path]:
    documents: list[Path] = []
    folders, markdown_files = sorted_children(folder)
    for child_folder in folders:
        documents.extend(collect_documents(child_folder))
    documents.extend(markdown_files)
    return documents


def build_listing_entries(section_slug: str, section_root: Path, folder: Path, current_file: Path) -> list[dict[str, str]]:
    folders, markdown_files = sorted_children(folder)
    entries: list[dict[str, str]] = []
    for child_folder in folders:
        entries.append(
            {
                "kind": "folder",
                "title": child_folder.name,
                "url": relative_url(current_file, output_for_folder(section_slug, section_root, child_folder)),
            }
        )
    for source in markdown_files:
        entries.append(
            {
                "kind": "markdown",
                "title": source.stem,
                "url": relative_url(current_file, output_for_markdown(section_slug, section_root, source)),
            }
        )
    return entries


def render_listing(
    env: Environment,
    data: dict,
    page: dict,
    section_root: Path,
    folder: Path,
    output_file: Path,
) -> None:
    template = env.get_template("listing.html.j2")
    folder_title = page["title"] if folder == section_root else folder.name
    relative_folder = folder.relative_to(section_root)
    breadcrumb = [
        {"title": page["title"], "url": relative_url(output_file, output_for_folder(page["slug"], section_root, section_root))}
    ]
    if str(relative_folder) != ".":
        running = section_root
        for part in relative_folder.parts:
            running = running / part
            breadcrumb.append(
                {
                    "title": part,
                    "url": relative_url(output_file, output_for_folder(page["slug"], section_root, running)),
                }
            )
    html = template.render(
        **data,
        page=page,
        subtitle=folder_title,
        math=False,
        body_class="inner-page listing-page",
        asset_prefix=asset_prefix(output_file),
        listing_title=folder_title,
        breadcrumb=breadcrumb,
        entries=build_listing_entries(page["slug"], section_root, folder, output_file),
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html + "\n", encoding="utf-8", newline="\n")


def render_section_tree(env: Environment, data: dict, page: dict) -> None:
    section_root = SRC / "content" / page["slug"]
    section_root.mkdir(parents=True, exist_ok=True)
    documents = collect_documents(section_root)
    article_template = env.get_template("article.html.j2")
    document_outputs = [output_for_markdown(page["slug"], section_root, source) for source in documents]

    def render_folder(folder: Path) -> None:
        render_listing(env, data, page, section_root, folder, output_for_folder(page["slug"], section_root, folder))
        folders, _ = sorted_children(folder)
        for child_folder in folders:
            render_folder(child_folder)

    render_folder(section_root)

    for index, source in enumerate(documents):
        output_file = document_outputs[index]
        previous_doc = None
        next_doc = None
        if index > 0:
            previous_doc = {
                "title": documents[index - 1].stem,
                "url": relative_url(output_file, document_outputs[index - 1]),
            }
        if index < len(documents) - 1:
            next_doc = {
                "title": documents[index + 1].stem,
                "url": relative_url(output_file, document_outputs[index + 1]),
            }
        html = article_template.render(
            **data,
            page=page,
            article_title=source.stem,
            subtitle=f"{page['title']} / {source.stem}",
            math=page.get("math", False),
            body_class="inner-page article-page",
            asset_prefix=asset_prefix(output_file),
            content=render_markdown(source),
            previous_doc=previous_doc,
            next_doc=next_doc,
            index_url=relative_url(output_file, output_for_folder(page["slug"], section_root, source.parent)),
        )
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html + "\n", encoding="utf-8", newline="\n")


def render_site() -> None:
    data = json.loads((SRC / "content" / "site.json").read_text(encoding="utf-8"))
    env = Environment(
        loader=FileSystemLoader(SRC / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    copy_static_assets()
    remove_managed_outputs()
    data["asset_version"] = static_asset_version()

    template = env.get_template("index.html.j2")
    html = template.render(
        **data,
        subtitle=data["home"]["subtitle"],
        math=False,
        body_class="home-page",
        asset_prefix="",
    )
    (ROOT / "index.html").write_text(html + "\n", encoding="utf-8", newline="\n")

    page_template = env.get_template("page.html.j2")
    for page in data["pages"]:
        if page["slug"] in MANAGED_SECTIONS:
            render_section_tree(env, data, page)
            continue
        content = render_markdown(SRC / "content" / page["source"])
        html = page_template.render(
            **data,
            page=page,
            subtitle=page["subtitle"],
            math=page.get("math", False),
            body_class="inner-page",
            asset_prefix="",
            content=content,
        )
        (ROOT / f"{page['slug']}.html").write_text(html + "\n", encoding="utf-8", newline="\n")

    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    render_site()
    print("Generated static pages and assets/ for GitHub Pages.")
