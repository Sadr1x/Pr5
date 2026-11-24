"""Генерує файл залежностей або перевіряє його в іншому середовищі."""

import argparse
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import subprocess
import sys

BOOTSTRAP_PACKAGES = {"pip", "setuptools", "wheel"}


def get_installed_packages() -> list[dict]:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def generate_requirements(packages: list[dict], filename: str = "requirements.txt"):
    lines = [
        f"{package['name']}=={package['version']}\n"
        for package in sorted(packages, key=lambda item: item["name"].lower())
        if package["name"].lower() not in BOOTSTRAP_PACKAGES
    ]
    Path(filename).write_text("".join(lines), encoding="utf-8")


def verify_requirements(filename: str = "requirements.txt") -> bool:
    try:
        lines = Path(filename).read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
        return False

    ok = True
    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.partition("#")[0].strip()
        if not line:
            continue
        name, separator, expected = (part.strip() for part in line.partition("=="))
        if not separator or not name or not expected:
            print(f"Рядок {number}: очікується формат package==version.")
            ok = False
            continue
        try:
            installed = version(name)
        except PackageNotFoundError:
            print(f"  {name} відсутній.")
            ok = False
            continue
        if installed != expected:
            print(f"  {name}: встановлено {installed}, потрібно {expected}.")
            ok = False
    return ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Перевірити без перезапису")
    parser.add_argument("--file", default="requirements.txt", help="Шлях до файлу")
    args = parser.parse_args()

    # У другому venv перевіряємо вихідні версії без перезапису файлу.
    if not args.check:
        packages = get_installed_packages()
        print(f"Знайдено пакетів (разом зі службовими): {len(packages)}")
        generate_requirements(packages, args.file)
        print(f"Створено файл {args.file}")

    ok = verify_requirements(args.file)
    print("Перевірка залежностей: " + ("усе гаразд" if ok else "є розбіжності"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
