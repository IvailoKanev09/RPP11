""""chetim.py — същата логика като nechetim.py, разделена на ясни функции."""


def izchisli_sreden_uspeh(ocenki):
    """Връща средния успех от списък с оценки или None при празен списък."""
    if not ocenki:
        return None
    return sum(ocenki) / len(ocenki)


def filtriraj_po_sreden_uspeh(uchenici_ocenki, prag):
    """Връща списък от (име, среден_успех) за ученици със среден успех >= prag."""
    rezultati = []
    for ime, ocenki in uchenici_ocenki.items():
        sreden_uspeh = izchisli_sreden_uspeh(ocenki)
        if sreden_uspeh is not None and sreden_uspeh >= prag:
            rezultati.append((ime, sreden_uspeh))
    return rezultati


if __name__ == "__main__":
    uchenici = {
        "Ани": [6, 5, 6, 4],
        "Борис": [3, 4, 3],
        "Валентин": [5, 6, 6, 5],
        "Георги": [],
        "Диана": [6, 6, 6],
    }
    print(filtriraj_po_sreden_uspeh(uchenici, 5.0))
    print(filtriraj_po_sreden_uspeh(uchenici, 5.5))
    print(filtriraj_po_sreden_uspeh({}, 4.0))