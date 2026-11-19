"""ariane.py — полетът, който можеше да не завърши така.

Опростен модел на това, което се случва на борда на Ariane 5.
Задача 2.1: следвайте стъпките в README.md на урока.
"""

INT16_MIN = -32_768
INT16_MAX = 32_767


class OverflowAlarm(Exception):
    """Собствено изключение: стойността не се побира в 16 бита."""

    def __init__(self, value):
        super().__init__(f"Стойност {value:.1f} не се побира в 16-битово цяло")
        self.value = value


def to_int16(value: float) -> int:
    """Преобразува 64-битово дробно число към 16-битово цяло със знак.

    Ако стойността е извън диапазона INT16_MIN..INT16_MAX,
    вдига OverflowAlarm.
    """
    converted = int(value)
    if converted < INT16_MIN or converted > INT16_MAX:
        raise OverflowAlarm(value)
    return converted


def horizontal_bias(t: float, acceleration: float) -> float:
    """Опростен модел на хоризонталното отклонение BH след t секунди."""
    return 0.5 * acceleration * t * t


def flight(
    rocket: str,
    acceleration: float,
    duration: int,
    mode: str = "clamp",
) -> None:
    """Симулира полет от duration секунди и печата какво стига до автопилота."""
    print(f"\n--- Полет на {rocket} [режим: {mode}] ---")
    for t in range(1, duration + 1):
        bh = horizontal_bias(t, acceleration)
        try:
            value = to_int16(bh)
        except OverflowAlarm as exc:
            if mode == "crash":
                raise
            if mode == "clamp":
                value = INT16_MAX if bh > INT16_MAX else INT16_MIN
                print(f"  [ПРЕДУПРЕЖДЕНИЕ t={t}s] {exc} -> ограничено до {value}")
            elif mode == "int32":
                value = int(bh)
                print(f"  [ПРЕДУПРЕЖДЕНИЕ t={t}s] {exc} -> преминато към int32: {value}")
            else:
                raise ValueError(f"Непознат режим: {mode}") from exc
        print(f"  t={t:2d}s  BH={bh:10.1f}  -> към автопилота: {value}")
    print("  Полетът завърши успешно.")


if __name__ == "__main__":
    flight("Ariane 4", acceleration=45.0, duration=10, mode="crash")
    flight("Ariane 5 (clamp)", acceleration=900.0, duration=10, mode="clamp")
    flight("Ariane 5 (int32)", acceleration=900.0, duration=10, mode="int32")