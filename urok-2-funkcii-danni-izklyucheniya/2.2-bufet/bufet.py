"""bufet.py — училищният бюфет: речници, функции и йерархия от изключения.

Задача 2.2: разширете модула с функциите от README.md на урока.
"""

STOCK = {
    "банан":   {"cena": 1.20, "kolichestvo": 10},
    "кроасан": {"cena": 2.50, "kolichestvo": 4},
    "вода":    {"cena": 0.90, "kolichestvo": 25},
    "сандвич": {"cena": 3.80, "kolichestvo": 0},
}


class BufetError(Exception):
    """Базово изключение на бюфета — всички останали наследяват него."""


class UnknownProduct(BufetError):
    pass


class NotEnoughStock(BufetError):
    def __init__(self, name, wanted, available):
        super().__init__(f"Искаш {wanted} бр. '{name}', а има само {available} бр.")
        self.name, self.wanted, self.available = name, wanted, available


class PriceError(BufetError):
    """Изключение при невалидна (отрицателна или нулева) цена."""

    def __init__(self, price):
        super().__init__(f"Невалидна цена: {price:.2f} лв. (трябва да е > 0)")
        self.price = price


def sell(stock: dict, name: str, quantity: int) -> float:
    """Продава quantity броя от name. Връща сумата."""
    if name not in stock:
        raise UnknownProduct(f"Няма продукт '{name}' в бюфета")
    if quantity <= 0:
        raise ValueError("Количеството трябва да е положително цяло число")
    item = stock[name]
    if item["kolichestvo"] < quantity:
        raise NotEnoughStock(name, quantity, item["kolichestvo"])
    item["kolichestvo"] -= quantity
    return round(item["cena"] * quantity, 2)


def receipt(stock: dict, order: list) -> tuple:
    """Обработва поръчка. Връща (сума, редове на бележката, проблеми)."""
    total, lines, problems = 0.0, [], []
    for name, quantity in order:
        try:
            price = sell(stock, name, quantity)
        except BufetError as err:
            problems.append(str(err))
        except ValueError as err:
            problems.append(f"Невалидно количество за '{name}': {err}")
        else:
            total += price
            lines.append(f"{name:10s} x{quantity:2d} = {price:6.2f} лв.")
    return round(total, 2), lines, problems


def low_stock(stock: dict, threshold: int = 5) -> list:
    """Имена на продуктите, които трябва да се доставят."""
    return sorted(name for name, item in stock.items()
                  if item["kolichestvo"] <= threshold)


def deliver(stock: dict, name: str, quantity: int, cena: float = None) -> int:
    """Добавя quantity броя от продукт и връща новата наличност."""
    if quantity <= 0:
        raise ValueError("Доставеното количество трябва да е положително")

    if name not in stock:
        if cena is None:
            raise UnknownProduct(f"Нов продукт '{name}' изисква зададена цена")
        if cena <= 0:
            raise PriceError(cena)
        stock[name] = {"cena": round(cena, 2), "kolichestvo": quantity}
        return stock[name]["kolichestvo"]

    if cena is not None:
        if cena <= 0:
            raise PriceError(cena)
        stock[name]["cena"] = round(cena, 2)

    stock[name]["kolichestvo"] += quantity
    return stock[name]["kolichestvo"]


def apply_discount(total: float, is_teacher: bool) -> float:
    """Прилага 10% отстъпка за учители и закръгля до стотинка."""
    if is_teacher:
        return round(total * 0.9, 2)
    return round(total, 2)


def daily_report(stock: dict) -> dict:
    """Връща дневен отчет за наличностите и стойността в бюфета."""
    if not stock:
        return {
            "obshta_stoynost": 0.0,
            "nay_skap": None,
            "izcherpani": 0,
        }

    total_value = round(
        sum(item["cena"] * item["kolichestvo"] for item in stock.values()),
        2,
    )
    most_expensive = max(stock, key=lambda name: stock[name]["cena"])
    out_of_stock = sum(1 for item in stock.values() if item["kolichestvo"] == 0)

    return {
        "obshta_stoynost": total_value,
        "nay_skap": most_expensive,
        "izcherpani": out_of_stock,
    }


if __name__ == "__main__":
    order = [("банан", 2), ("кроасан", 1), ("сандвич", 1),
             ("пица", 1), ("вода", -3), ("вода", 2)]
    total, lines, problems = receipt(STOCK, order)

    print("КАСОВА БЕЛЕЖКА")
    for line in lines:
        print("  " + line)
    print(f"  ОБЩО: {total:.2f} лв.")

    if problems:
        print("\nНЕИЗПЪЛНЕНИ ПОЗИЦИИ:")
        for problem in problems:
            print(f"  - {problem}")

    print(f"\nЗА ДОСТАВКА: {', '.join(low_stock(STOCK))}")

    print("\n--- СЦЕНАРИИ ЗА ЗАДАЧА 2.2 ---")

    # 1. Доставка на съществуващ продукт
    new_qty = deliver(STOCK, "сандвич", 6)
    print(f"1. Доставка сандвич -> нова наличност: {new_qty} бр.")

    # 2. Доставка на нов продукт с валидна цена
    new_qty = deliver(STOCK, "солети", 15, cena=1.10)
    print(f"2. Нов продукт 'солети' -> наличност: {new_qty} бр.")

    # 3. Изчисление на отстъпка за учител и ученик
    print(f"3. Сметка 12.50 лв.: учител = {apply_discount(12.50, True):.2f} лв., "
          f"ученик = {apply_discount(12.50, False):.2f} лв.")

    # 4. Грешка 1: Нов продукт без цена -> UnknownProduct
    try:
        deliver(STOCK, "вафла", 10)
    except UnknownProduct as err:
        print(f"4. Очаквано изключение (UnknownProduct): {err}")

    # 5. Грешка 2: Отрицателна/нулева цена -> PriceError
    try:
        deliver(STOCK, "вафла", 10, cena=-1.50)
    except PriceError as err:
        print(f"5. Очаквано изключение (PriceError): {err}")

    # 6. Грешка 3: Невалидно количество при доставка -> ValueError
    try:
        deliver(STOCK, "банан", 0)
    except ValueError as err:
        print(f"6. Очаквано изключение (ValueError): {err}")

    # 7. Дневен отчет
    report = daily_report(STOCK)
    print(f"7. Дневен отчет: {report}")