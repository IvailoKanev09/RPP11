"""detektiv.py — в какво кодиране е записан файлът?

Задача 3.1. Четирите файла tekst_a.txt … tekst_d.txt съдържат един
и същ текст, но са записани в различни кодирания.
"""
from pathlib import Path

HERE = Path(__file__).parent
FILES = ["tekst_a.txt", "tekst_b.txt", "tekst_c.txt", "tekst_d.txt"]
ENCODINGS = ["utf-8", "cp1251", "utf-16", "latin-1"]

# Знаци, които почти никога не се срещат в български текст,
# но са типични за mojibake. Допълнете списъка, ако е нужно.
SUSPICIOUS = "ÃÐÑñÿÇäðàâåé"


def _has_bulgarian_letters(text: str) -> bool:
    """Проверява дали в текста има поне една българска буква (кирилица)."""
    return any(("А" <= ch <= "Я") or ("а" <= ch <= "я") or ch in ("Й", "й", "Ъ", "ъ", "Ь", "ь") for ch in text)


def _has_suspicious_chars(text: str) -> bool:
    """Проверява дали в текста има знаци от SUSPICIOUS."""
    return any(ch in SUSPICIOUS for ch in text)


def preview(path, encoding: str, n: int = 40) -> str:
    """Първите n символа от файла, прочетен с даденото кодиране.

    Ако файлът не може да се прочете с това кодиране,
    UnicodeDecodeError не се прехваща тук — нека реши викащият.
    """
    with open(path, encoding=encoding) as file:
        text = file.read(n)
    return repr(text)


def guess_encoding(path):
    """Името на първото кодиране от ENCODINGS, при което текстът
    съдържа български букви и няма знаци от SUSPICIOUS.
    None, ако нито едно не пасва.
    """
    for enc in ENCODINGS:
        try:
            with open(path, encoding=enc) as file:
                text = file.read()
        except UnicodeDecodeError:
            continue

        if _has_bulgarian_letters(text) and not _has_suspicious_chars(text):
            return enc

    return None


def main() -> None:
    for name in FILES:
        file_path = HERE / name
        print(f"\n=== {name} ===")
        for enc in ENCODINGS:
            try:
                sample = preview(file_path, enc, n=40)
            except UnicodeDecodeError:
                print(f"  {enc:8s} -> не става (UnicodeDecodeError)")
            else:
                print(f"  {enc:8s} -> {sample}")

        guessed = guess_encoding(file_path)
        print(f"  Догадка: {guessed}")


if __name__ == "__main__":
    main()

# СТЪПКА 4: кога методът ви би сгрешил? Отговорете тук в коментар.
# Методът може да сгреши в няколко случая:
# 1. При много кратък текст или текст без български букви (например само цифри,
#    латиница или символи) — тогава _has_bulgarian_letters връща False и догадката е None.
# 2. Ако в истински български текст случайно има знак от SUSPICIOUS (или ако кодирането
#    създаде mojibake с кирилски символи, които не са в SUSPICIOUS, например при размяна
#    между CP1251 и MIK), проверката може да пропусне грешката или да отхвърли валиден текст.
# 3. При UTF-16 без BOM (или при специфични байтови комбинации) latin-1 никога не вдига
#    UnicodeDecodeError, защото всеки байт 0x00..0xFF е валиден символ в latin-1.