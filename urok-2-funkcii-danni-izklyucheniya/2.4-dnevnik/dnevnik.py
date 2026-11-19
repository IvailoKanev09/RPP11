"""dnevnik.py — среден успех и класация от речник с оценки.

Задача 2.4. Данните имат вида:

    {"име": {"предмет": [оценки], ...}, ...}

Нито една функция не бива да гърми при ученик без оценки
или при празен речник. Функциите връщат резултат и не печатат.
"""

STUDENTS = {
    "Ани":    {"математика": [6, 5, 6], "български": [5, 6], "история": [6]},
    "Борис":  {"математика": [3, 2, 4], "български": [3], "история": [4, 3]},
    "Вера":   {"математика": [5, 5], "български": [6, 6], "история": []},
    "Георги": {},
    "Диана":  {"математика": [2, 3], "български": [3, 4], "история": [3]},
}


def subject_average(student: dict, subject: str):
    """Среден успех по предмет. None, ако предметът липсва или няма оценки."""
    if not student or subject not in student:
        return None
    grades = student[subject]
    if not grades:
        return None
    return sum(grades) / len(grades)


def overall_average(student: dict):
    """Общ успех: средно аритметично на средните успехи по предмети.

    Предмети без оценки не участват. None, ако ученикът няма нито една оценка.
    """
    if not student:
        return None
    averages = [
        avg for subject in student
        if (avg := subject_average(student, subject)) is not None
    ]
    if not averages:
        return None
    return sum(averages) / len(averages)


def weakest_subject(student: dict):
    """Предметът с най-нисък среден успех. None, ако няма оценки.

    При равенство — първият по азбучен ред.
    """
    if not student:
        return None
    subject_avgs = {
        subject: avg for subject in student
        if (avg := subject_average(student, subject)) is not None
    }
    if not subject_avgs:
        return None
    return min(subject_avgs.keys(), key=lambda subj: (subject_avgs[subj], subj))


def class_ranking(students: dict) -> list:
    """Списък от (име, общ успех), подреден от най-високия към най-ниския.

    Учениците без оценки са накрая (с успех None), подредени по азбучен ред.
    При равен успех — по азбучен ред на името.
    """
    if not students:
        return []

    rows = [(name, overall_average(data)) for name, data in students.items()]

    def sort_key(item):
        name, avg = item
        if avg is None:
            return (1, 0.0, name)
        return (0, -avg, name)

    return sorted(rows, key=sort_key)


def at_risk(students: dict, threshold: float = 3.50) -> list:
    """Имената (по азбучен ред) на учениците с общ успех под threshold.

    Ученици без оценки не се включват — за тях няма данни.
    """
    if not students:
        return []

    risky = [
        name for name, data in students.items()
        if (avg := overall_average(data)) is not None and avg < threshold
    ]
    return sorted(risky)


if __name__ == "__main__":
    assert subject_average(STUDENTS["Ани"], "история") == 6
    assert subject_average(STUDENTS["Георги"], "история") is None
    assert subject_average(STUDENTS["Вера"], "история") is None
    assert overall_average(STUDENTS["Георги"]) is None
    assert overall_average(STUDENTS["Вера"]) == 5.5
    assert weakest_subject(STUDENTS["Борис"]) == "български"
    assert weakest_subject(STUDENTS["Георги"]) is None
    assert class_ranking({}) == []
    assert at_risk(STUDENTS) == ["Борис", "Диана"]
    assert at_risk(STUDENTS, threshold=3.0) == []