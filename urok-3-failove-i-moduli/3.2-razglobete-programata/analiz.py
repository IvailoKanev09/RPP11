"""analiz.py — чиста логика за анализ на продажбите (без файлове и печат)."""
import datetime

DAYS = ["понеделник", "вторник", "сряда", "четвъртък", "петък", "събота", "неделя"]


def oborot_po_produkti(prodazhbi: list[dict]) -> dict[str, float]:
    """Връща речник {продукт: общ_оборот}."""
    rezultat = {}
    for p in prodazhbi:
        suma = p["broy"] * p["cena"]
        rezultat[p["produkt"]] = rezultat.get(p["produkt"], 0.0) + suma
    return rezultat


def oborot_po_dni(prodazhbi: list[dict]) -> tuple[dict[str, float], str | None]:
    """Връща (речник {дата: оборот}, датата_на_най_добрия_ден)."""
    rezultat = {}
    for p in prodazhbi:
        rezultat[p["data"]] = rezultat.get(p["data"], 0.0) + p["broy"] * p["cena"]

    nay_dobur = None
    for data in sorted(rezultat):
        if nay_dobur is None or rezultat[data] > rezultat[nay_dobur]:
            nay_dobur = data

    return rezultat, nay_dobur


def den_ot_sedmitsata(iso_date: str) -> str:
    """Връща името на деня от седмицата на български за ISO дата (ГГГГ-ММ-ДД)."""
    return DAYS[datetime.date.fromisoformat(iso_date).weekday()]


def nay_prodavan(prodazhbi: list[dict]) -> tuple[str, int, float] | None:
    """Връща (най-продаван_продукт, бройки_на_най-продавания, средно_бройки_на_продукт)."""
    if not prodazhbi:
        return None

    broyki = {}
    for p in prodazhbi:
        broyki[p["produkt"]] = broyki.get(p["produkt"], 0) + p["broy"]

    nay = ""
    for produkt in broyki:
        if nay == "" or broyki[produkt] > broyki[nay]:
            nay = produkt

    sredno = sum(broyki.values()) / len(broyki)
    return nay, broyki[nay], sredno


def obsht_oborot(prodazhbi: list[dict]) -> float:
    """Изчислява общия оборот от всички продажби."""
    return sum(p["broy"] * p["cena"] for p in prodazhbi)


if __name__ == "__main__":
    sample = [
        {"data": "2026-11-02", "produkt": "банан", "broy": 10, "cena": 1.2},
        {"data": "2026-11-02", "produkt": "вода", "broy": 20, "cena": 1.0},
        {"data": "2026-11-03", "produkt": "банан", "broy": 5, "cena": 1.2},
    ]

    # 1. Оборот по продукти
    assert oborot_po_produkti(sample) == {"банан": 18.0, "вода": 20.0}

    # 2. Оборот по дни и най-добър ден
    po_dni, best_day = oborot_po_dni(sample)
    assert po_dni == {"2026-11-02": 32.0, "2026-11-03": 6.0}
    assert best_day == "2026-11-02"

    # 3. Най-продаван продукт и средни бройки
    assert nay_prodavan(sample) == ("вода", 20, 17.5)

    # 4. Общ оборот
    assert obsht_oborot(sample) == 38.0

    # 5. Празен списък не гърми
    assert nay_prodavan([]) is None
    assert obsht_oborot([]) == 0