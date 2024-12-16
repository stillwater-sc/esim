import math


def scientific_format(value: float, dimension: str) -> str:
    """

    Args:
        value: floating-point value to convert

    Returns: str

    """
    if value == 0.0:
        return f"{value:7.3f} {dimension}"

    value = math.fabs(value)
    if value >= 1.0:
        if 1.0e0 <= value < 1000.0:
            return f"{value:7.3f} {dimension}"
        elif 1.0e3 <= value < 1.0e6:
            return f"{value/1.0e3:7.3f} k{dimension}"
        elif 1.0e6 <= value < 1.0e9:
            return f"{value/1.0e6:7.3f} M{dimension}"
        elif 1.0e9 <= value < 1.0e12:
            return f"{value/1.0e9:7.3f} G{dimension}"
        elif 1.0e12 <= value < 1.0e15:
            return f"{value/1.0e12:7.3f} T{dimension}"
        elif 1.0e15 <= value < 1.0e18:
            return f"{value/1.0e15:7.3f} P{dimension}"
        elif 1.0e18 <= value < 1.0e21:
            return f"{value/1.0e18:7.3f} E{dimension}"
        else:
            return f"{value / 1.0e24:7.3f} Z{dimension}"
    else:
        if 1.0e-3 <= value < 1.0e0:
            return f"{value/1.0e-3:7.3f} m{dimension}"
        elif 1.0e-6 <= value < 1.0e-3:
            return f"{value/1.0e-6:7.3f} u{dimension}"
        elif 1.0e-9 <= value < 1.0e-6:
            return f"{value/1.0e-9:7.3f} n{dimension}"
        elif 1.0e-12 <= value < 1.0e-9:
            return f"{value/1.0e-12:7.3f} p{dimension}"
        elif 1.0e-15 <= value < 1.0e-12:
            return f"{value/1.0e-15:7.3f} f{dimension}"
        else:
            return f"{value/1.0e-18:7.3f} a{dimension}"