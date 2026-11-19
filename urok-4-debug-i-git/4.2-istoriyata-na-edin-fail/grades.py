STUDENTS = {
    "Ани": [6, 5, 6, 4],
    "Борис": [3, 4, 3],
    "Валентин": [5, 6, 6, 5],
    "Вера": [5, 5, 6, 6, 5],
    "Георги": [],
    "Диана": [6, 6, 6],
}


def average(grades):
    if not grades:
        return None
    total = 0
    for g in grades:
        total += g
    return total / len(grades)


def median(grades):
    if not grades:
        return None
    ordered = sorted(grades)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2


def is_excellent(avg):
    return avg is not None and avg >= 5.50


def ranking(students):
    result = []
    for name in students:
        result.append((name, average(students[name])))
    result.sort(key=lambda pair: (pair[1] is None, -(pair[1] or 0.0), pair[0]))
    return result


def print_report(students):
    print("КЛАСАЦИЯ")
    position = 0
    excellent_count = 0
    for name, avg in ranking(students):
        position += 1
        if avg is None:
            print(f"{position}. {name:10s} няма оценки")
            continue
        if is_excellent(avg):
            excellent_count += 1
            mark = " *"
        else:
            mark = ""
        print(f"{position}. {name:10s} {avg:.2f}{mark}")

    all_grades = []
    for name in students:
        all_grades.extend(students[name])

    class_avg = average(all_grades)
    if class_avg is not None:
        print(f"Среден успех на класа: {class_avg:.2f}")
    else:
        print("Среден успех на класа: няма оценки")
    print(f"Брой отличници: {excellent_count}")


if __name__ == "__main__":
    print_report(STUDENTS)
    top_student = ranking(STUDENTS)[0][0]
    print(f"Най-добър ученик: {top_student}")