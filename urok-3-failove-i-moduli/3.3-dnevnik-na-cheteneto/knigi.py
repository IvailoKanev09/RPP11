"""knigi.py — дневник на прочетените книги в текстов файл.

Задача 3.3. Един ред във файла е една книга:

    заглавие | автор | година на прочитане | оценка от 1 до 6

Правила: файлът се отваря само с with и само с явно кодиране;
повреден ред не спира програмата.
"""
from pathlib import Path

HERE = Path(__file__).parent
KNIGI = HERE / "knigi.txt"


def add_book(path, title: str, author: str, year: int, rating: int) -> None:
    """Добавя ред в края на файла, без да презаписва старите.

    При оценка извън 1..6 вдига ValueError и не пише нищо.
    """
    if not isinstance(rating, int) or isinstance(rating, bool) or not (1 <= rating <= 6):
        raise ValueError(f"Оценката трябва да е цяло число от 1 до 6, получено: {rating}")

    file_path = Path(path)
    needs_newline = False
    if file_path.exists() and file_path.stat().st_size > 0:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            if content and not content.endswith("\n"):
                needs_newline = True

    with open(file_path, "a", encoding="utf-8") as f:
        if needs_newline:
            f.write("\n")
        f.write(f"{title} | {author} | {year} | {rating}\n")


def load_books(path) -> tuple:
    """Чете файла. Връща (книги, брой_пропуснати_редове).

    Всяка книга е речник с ключове "zaglavie", "avtor",
    "godina" (int) и "otsenka" (int).
    Пропуска повредените редове: с друг брой полета, с година
    или оценка, която не е число, или с оценка извън 1..6.
    Ако файлът липсва, дневникът е празен: връща ([], 0).
    """
    file_path = Path(path)
    if not file_path.exists():
        return [], 0

    books = []
    skipped = 0

    with open(file_path, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [part.strip() for part in line.split("|")]
            if len(parts) != 4:
                skipped += 1
                continue

            title, author, year_str, rating_str = parts
            if not title or not author:
                skipped += 1
                continue

            try:
                year = int(year_str)
                rating = int(rating_str)
            except ValueError:
                skipped += 1
                continue

            if not (1 <= rating <= 6):
                skipped += 1
                continue

            books.append({
                "zaglavie": title,
                "avtor": author,
                "godina": year,
                "otsenka": rating,
            })

    return books, skipped


def stats(books: list) -> dict:
    """Връща речник с ключове:

    "sredna_otsenka" — средната оценка (None при празен списък),
    "nay_dobra"      — заглавието с най-висока оценка
                       (при равенство — първото във файла; None при празен списък),
    "po_godini"      — речник {година: брой книги}.
    """
    if not books:
        return {
            "sredna_otsenka": None,
            "nay_dobra": None,
            "po_godini": {},
        }

    total_rating = sum(book["otsenka"] for book in books)
    avg_rating = total_rating / len(books)

    best_book = books[0]
    for book in books[1:]:
        if book["otsenka"] > best_book["otsenka"]:
            best_book = book

    by_year = {}
    for book in books:
        year = book["godina"]
        by_year[year] = by_year.get(year, 0) + 1

    return {
        "sredna_otsenka": avg_rating,
        "nay_dobra": best_book["zaglavie"],
        "po_godini": by_year,
    }


def export_report(path, books: list) -> None:
    """Записва подреден текстов отчет в UTF-8."""
    summary = stats(books)

    with open(path, "w", encoding="utf-8") as f:
        f.write("ДНЕВНИК НА ПРОЧЕТЕНИТЕ КНИГИ\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Общ брой книги: {len(books)}\n")

        if summary["sredna_otsenka"] is None:
            f.write("Средна оценка: няма данни\n")
            f.write("Най-добра книга: няма данни\n\n")
        else:
            f.write(f"Средна оценка: {summary['sredna_otsenka']:.2f}\n")
            f.write(f"Най-добра книга: {summary['nay_dobra']}\n\n")
            f.write("Книги по години:\n")
            for year in sorted(summary["po_godini"]):
                f.write(f"  {year}: {summary['po_godini'][year]} бр.\n")
            f.write("\nСписък с прочетени книги:\n")
            for book in books:
                f.write(
                    f"  - {book['zaglavie']} ({book['avtor']}, {book['godina']}) "
                    f"— оценка {book['otsenka']}/6\n"
                )


if __name__ == "__main__":
    books, skipped = load_books(KNIGI)
    print(f"Заредени {len(books)} книги, пропуснати {skipped} повредени реда.")
    report_data = stats(books)
    print(f"Средна оценка: {report_data['sredna_otsenka']:.2f}")
    print(f"Най-добра книга: {report_data['nay_dobra']}")
    print(f"По години: {report_data['po_godini']}")