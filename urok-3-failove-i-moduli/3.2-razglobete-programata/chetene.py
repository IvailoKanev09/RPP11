"""chetene.py — четене на продажби и запис на седмичен отчет."""
from pathlib import Path


def zaredi_prodazhbi(path: Path) -> tuple[list[dict], list[str], int]:
    """Чете продажби от файл и връща (списък продажби, съобщения за пропуснати редове, брой пропуснати)."""
    prodazhbi = []
    warnings = []
    propusnati = 0

    with open(path, encoding="utf-8") as f:
        for nomer, red in enumerate(f, start=1):
            red = red.strip()
            if not red or red.startswith("#"):
                continue
            chasti = [c.strip() for c in red.split("|")]
            if len(chasti) != 4:
                warnings.append(f"  Ред {nomer}: очаквах 4 полета, а са {len(chasti)} — пропускам")
                propusnati += 1
                continue
            data, produkt, broy_str, cena_str = chasti
            try:
                broy = int(broy_str)
                cena = float(cena_str)
            except ValueError:
                warnings.append(f"  Ред {nomer}: '{broy_str}' или '{cena_str}' не е число — пропускам")
                propusnati += 1
                continue
            prodazhbi.append({
                "data": data,
                "produkt": produkt,
                "broy": broy,
                "cena": cena,
            })

    return prodazhbi, warnings, propusnati


def zapishi_otchet(path: Path, obshto: float, po_produkti: dict, po_dni: dict) -> None:
    """Записва текстовия отчет за седмицата в UTF-8."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("ОТЧЕТ ЗА СЕДМИЦАТА\n")
        f.write(f"Общ оборот: {obshto:.2f} лв.\n\n")
        f.write("По продукти:\n")
        for produkt, suma in sorted(po_produkti.items(), key=lambda x: -x[1]):
            f.write(f"  {produkt}: {suma:.2f} лв.\n")
        f.write("\nПо дни:\n")
        for data in sorted(po_dni):
            f.write(f"  {data}: {po_dni[data]:.2f} лв.\n")