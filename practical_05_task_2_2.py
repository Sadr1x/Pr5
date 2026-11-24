"""Показує параметри settings.py та перевіряє три базові правила."""

import argparse
import ast
from pathlib import Path
import runpy
import sys


def analyze_settings(settings_path: str) -> dict:
    # Виконуємо довірений локальний модуль, щоб врахувати змінні оточення.
    config = runpy.run_path(settings_path)
    return {
        "DEBUG": config["DEBUG"],
        "INSTALLED_APPS": config["INSTALLED_APPS"],
        "DATABASES": config["DATABASES"]["default"]["ENGINE"],
        "LANGUAGE_CODE": config["LANGUAGE_CODE"],
        "TIME_ZONE": config["TIME_ZONE"],
    }


def check_security(settings_path: str) -> list[str]:
    config = runpy.run_path(settings_path)
    tree = ast.parse(Path(settings_path).read_text(encoding="utf-8"))
    warnings = []
    if config["DEBUG"]:
        warnings.append("DEBUG увімкнено. Для production його потрібно вимкнути.")
    if config["SECRET_KEY"] and any(
        isinstance(node, ast.Constant) and node.value == config["SECRET_KEY"]
        for node in ast.walk(tree)
    ):
        warnings.append("SECRET_KEY задано рядком у вихідному коді.")
    if not config["ALLOWED_HOSTS"]:
        warnings.append("ALLOWED_HOSTS порожній.")
    return warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("settings", nargs="?", default="mysite/mysite/settings.py")
    args = parser.parse_args()
    if not Path(args.settings).is_file():
        print(f"Файл {args.settings} не знайдено.")
        return 1

    print("=== Аналіз конфігурації Django ===")
    for key, value in analyze_settings(args.settings).items():
        if key == "INSTALLED_APPS":
            print(f"  {key}:")
            for app in value:
                print(f"    - {app}")
        else:
            print(f"  {key}: {value}")

    print("\n=== Перевірка безпеки ===")
    for warning in check_security(args.settings) or ["Попереджень не знайдено."]:
        print(f"  {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
