"""load_config.py — чете настройки от вида ключ=число.

Задача 2.3: в тази функция има четири проблема. Намерете ги,
опишете ги в otgovori.md и напишете поправена версия тук.
"""
from pathlib import Path

HERE = Path(__file__).parent  # папката на този файл, откъдето и да го стартирате


"""load_config.py — зареждане на конфигурация от текстов файл."""


def load_config(path) -> dict:
    """Зарежда конфигурация от файл с формат ключ=стойност (цели числа).

    Пропуска празни редове и коментари (#).
    Вдига ValueError при невалиден ред или нечислова стойност, като посочва номера на реда.
    Не прехваща FileNotFoundError и системни/потребителски прекъсвания като KeyboardInterrupt.
    """
    config = {}

    with open(path, encoding="utf-8") as file:
        for line_no, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Ред {line_no}: липсва '=' в реда {line!r}")

            raw_key, raw_val = line.split("=", 1)
            key = raw_key.strip()
            val_str = raw_val.strip()

            if not key:
                raise ValueError(f"Ред {line_no}: празен ключ в реда {line!r}")

            try:
                config[key] = int(val_str)
            except ValueError as err:
                raise ValueError(
                    f"Ред {line_no}: стойността {val_str!r} за ключ '{key}' не е цяло число"
                ) from err

    return config