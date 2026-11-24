"""Перевіряє версію Python та наявність фреймворків."""

import importlib
from importlib.metadata import PackageNotFoundError, version
import sys


def check_python_version():
    current = sys.version_info
    print(f"Python {current.major}.{current.minor}.{current.micro}")
    if current < (3, 10):
        print("Попередження: потрібен Python 3.10 або новіший.")
        return False
    return True


def check_package(package_name: str) -> bool:
    try:
        importlib.import_module(package_name)
        package_version = version(package_name)
    except (ImportError, PackageNotFoundError):
        print(f"  {package_name}: не встановлено або не імпортується")
        return False

    print(f"  {package_name}: {package_version} [OK]")
    return True


def main():
    python_ok = check_python_version()
    print("\nВстановлені пакети:")
    packages = ("django", "flask")
    missing = [package for package in packages if not check_package(package)]
    print(f"\nВстановлено: {len(packages) - len(missing)}. Відсутні: {len(missing)}.")
    if missing:
        print("Команда для встановлення: python -m pip install " + " ".join(missing))
    return 0 if python_ok and not missing else 1


if __name__ == "__main__":
    sys.exit(main())
