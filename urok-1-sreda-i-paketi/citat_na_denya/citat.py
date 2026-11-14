"""citat.py — цитат на деня.

Цитатите се четат от файла data/citati.txt (формат: текст | автор),
а не са записани в кода. Програмата работи и без инсталиран пакет rich,
но тогава сама казва какво липсва.
"""
import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Пътят е спрямо самия файл citat.py, за да работи от всяка работна папка.
QUOTES_DATA_PATH = Path(__file__).parent / "data" / "citati.txt"


def load_quotes(file_path: Path) -> list:
    """Чете файла и връща списък от двойки (текст, автор)."""
    quote_list = []
    with open(file_path, encoding="utf-8") as source_file:
        for line_number, current_line in enumerate(source_file, start=1):
            current_line = current_line.strip()
            if not current_line:
                continue  # празните редове се пропускат
            if "|" not in current_line:
                raise ValueError(f"Ред {line_number} в {file_path.name} няма разделител '|': {current_line!r}")
            quote_text, quote_author = current_line.rsplit("|", 1)  # разделяме по последния '|'
            quote_list.append((quote_text.strip(), quote_author.strip()))
    if not quote_list:
        raise ValueError(f"Файлът {file_path.name} не съдържа цитати.")
    return quote_list


def quote_of_the_day(quote_list: list, target_date: datetime.date) -> tuple:
    """Един и същ цитат за целия ден, различен за всеки ден."""
    return quote_list[target_date.toordinal() % len(quote_list)]


def main() -> None:
    try:
        quote_collection = load_quotes(QUOTES_DATA_PATH)
    except (OSError, ValueError) as err:
        print(f"Грешка при четене на цитатите: {err}")
        return

    current_date = datetime.date.today()
    quote_text, quote_author = quote_of_the_day(quote_collection, current_date)

    if RICH_AVAILABLE:
        Console().print(Panel(f"[italic]{quote_text}[/italic]\n\n[bold]— {quote_author}[/bold]",
                              title=f"Цитат за {current_date:%d.%m.%Y}", border_style="cyan"))
    else:
        print("Пакетът 'rich' не е инсталиран в тази среда.")
        print("Направи:  python -m pip install -r requirements.txt")
        print(f"\n{quote_text}\n— {quote_author}")


if __name__ == "__main__":
    main()