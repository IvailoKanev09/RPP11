"""main.py — входна точка за анализа на продажбите в бюфета."""
from pathlib import Path

from analiz import (
    den_ot_sedmitsata,
    nay_prodavan,
    oborot_po_dni,
    oborot_po_produkti,
    obsht_oborot,
)
from chetene import zaredi_prodazhbi, zapishi_otchet

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "prodazhbi.txt"
REPORT_FILE = HERE / "otchet.txt"


def main() -> None:
    print("АНАЛИЗ НА ПРОДАЖБИТЕ В БЮФЕТА")
    prodazhbi, warnings, propusnati = zaredi_prodazhbi(DATA_FILE)
    for msg in warnings:
        print(msg)
    print(f"Заредени {len(prodazhbi)} продажби, пропуснати {propusnati} реда.")

    po_produkti = oborot_po_produkti(prodazhbi)
    print("\nОБОРОТ ПО ПРОДУКТИ")
    for produkt, suma in sorted(po_produkti.items(), key=lambda x: -x[1]):
        print(f"  {produkt:10s} {suma:8.2f} лв.")

    po_dni, nay_dobur = oborot_po_dni(prodazhbi)
    print("\nОБОРОТ ПО ДНИ")
    for data in sorted(po_dni):
        den = den_ot_sedmitsata(data)
        print(f"  {data}  {den:11s}{po_dni[data]:8.2f} лв.")
    print(f"  Най-добър ден: {nay_dobur}")

    top = nay_prodavan(prodazhbi)
    if top is not None:
        nay, broy, sredno = top
        print(f"\nНАЙ-ПРОДАВАН ПРОДУКТ: {nay} ({broy} бр.)")
        print(f"Средно продадени бройки на продукт: {sredno:.1f}")

    obshto = obsht_oborot(prodazhbi)
    print(f"\nОБЩ ОБОРОТ: {obshto:.2f} лв.")
    zapishi_otchet(REPORT_FILE, obshto, po_produkti, po_dni)
    print(f"Отчетът е записан в {REPORT_FILE.name}")


if __name__ == "__main__":
    main()