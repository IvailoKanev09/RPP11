"""env_check.py — „Кой Python работи в момента?“

Изпълнете програмата два пъти: веднъж с глобалния Python и веднъж
от активирана виртуална среда. Сравнете редовете „Текущ префикс“,
„Пакети в папка“ и „Брой пакети“.
"""
import importlib.metadata
import os
import platform
import site
import sys


def in_virtualenv() -> bool:
    """Връща True, ако програмата се изпълнява във виртуална среда."""
    return sys.prefix != sys.base_prefix


def site_packages_dirs() -> list[str]:
    """Папките, в които живеят инсталираните пакети на този Python."""
    try:
        dirs = site.getsitepackages()
    except AttributeError:
        # Много стари версии на virtualenv нямат getsitepackages()
        dirs = [p for p in sys.path if p.endswith("site-packages")]
    return dirs


def count_packages() -> int:
    """Брой различни инсталирани пакети (без повторения по име)."""
    names = {
        dist.metadata["Name"].lower().replace("_", "-")
        for dist in importlib.metadata.distributions()
        if dist.metadata["Name"]
    }
    return len(names)


def report() -> None:
    print("=" * 52)
    print("ДОКЛАД ЗА СРЕДАТА")
    print("=" * 52)
    print(f"Версия на Python : {platform.python_version()}")
    print(f"Изпълним файл    : {sys.executable}")
    print(f"Базов префикс    : {sys.base_prefix}")
    print(f"Текущ префикс    : {sys.prefix}")
    print(f"Работна папка    : {os.getcwd()}")
    for path in site_packages_dirs():
        print(f"Пакети в папка   : {path}")
    print(f"Брой пакети      : {count_packages()}")
    print("-" * 52)
    if in_virtualenv():
        print("СТАТУС: РАБОТИШ ВЪВ ВИРТУАЛНА СРЕДА.")
    else:
        print("СТАТУС: ГЛОБАЛЕН PYTHON — внимавай какво инсталираш!")
        print("ВНИМАНИЕ: НЕ СИ ВЪВ ВИРТУАЛНА СРЕДА! АКТИВИРАЙ СРЕДАТА ПРЕДИ ДА ИНСТАЛИРАШ ПАКЕТИ!")
    print("=" * 52)


if __name__ == "__main__":
    report()
