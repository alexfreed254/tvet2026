from datetime import datetime
from typing import Any


def serialize_datetime(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def format_percentage(value: float, decimals: int = 2) -> str:
    return f"{value:.{decimals}f}%"


def calculate_average(values: list) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)
