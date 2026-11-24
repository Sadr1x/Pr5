"""Порівнює дерево файлів і статистику проєктів Django та Flask."""

from pathlib import Path

IGNORED = {"__pycache__", "venv", "venv2", ".venv", ".git", "db.sqlite3"}


def project_entries(path: Path) -> list[Path]:
    # Спільний фільтр гарантує, що дерево і статистика враховують ті самі файли.
    entries = (
        child for child in path.iterdir()
        if child.name not in IGNORED
        and child.suffix != ".pyc"
        and not child.is_symlink()
    )
    return sorted(entries, key=lambda child: (not child.is_dir(), child.name.lower()))


def scan_directory(path: str, prefix: str = "") -> list[str]:
    tree = []
    entries = project_entries(Path(path))
    for index, entry in enumerate(entries):
        last = index == len(entries) - 1
        branch = "└── " if last else "├── "
        is_directory = entry.is_dir()
        label = entry.name + ("/" if is_directory else "")
        tree.append(prefix + branch + label)
        if is_directory:
            indent = "    " if last else "│   "
            tree.extend(scan_directory(str(entry), prefix + indent))
    return tree


def analyze_project(path: str) -> dict:
    root = Path(path)
    counters = {".py": "py_files", ".html": "html_files", ".css": "css_files"}
    stats = dict.fromkeys(counters.values(), 0)
    stats["total_size"] = 0
    stats["directories"] = []

    def collect(directory: Path):
        for entry in project_entries(directory):
            if entry.is_dir():
                stats["directories"].append(entry.relative_to(root).as_posix())
                collect(entry)
            elif entry.is_file():
                stats["total_size"] += entry.stat().st_size
                counter = counters.get(entry.suffix.lower())
                if counter:
                    stats[counter] += 1

    collect(root)
    return stats


def compare_projects(django_path: str, flask_path: str):
    print("ПОРІВНЯННЯ СТРУКТУРИ ПРОЄКТІВ")
    for label, path in (("Django", django_path), ("Flask", flask_path)):
        print(f"\n{label} ({path}/)")
        print("\n".join(scan_directory(path)))

    django = analyze_project(django_path)
    flask = analyze_project(flask_path)
    rows = [
        ("Файли .py", django["py_files"], flask["py_files"]),
        ("Файли .html", django["html_files"], flask["html_files"]),
        ("Файли .css", django["css_files"], flask["css_files"]),
        ("Каталоги", len(django["directories"]), len(flask["directories"])),
        ("Розмір (байт)", django["total_size"], flask["total_size"]),
    ]
    print(f"\n{'Характеристика':<18} | {'Django':>7} | {'Flask':>7}")
    print("-" * 38)
    for label, django_value, flask_value in rows:
        print(f"{label:<18} | {django_value:>7} | {flask_value:>7}")


def main():
    for path in ("mysite", "myflaskapp"):
        if not Path(path).is_dir():
            print(f"Каталог {path!r} не знайдено. Запустіть скрипт з кореня PR05.")
            return 1
    compare_projects("mysite", "myflaskapp")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
