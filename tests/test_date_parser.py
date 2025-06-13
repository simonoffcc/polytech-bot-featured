import pytest
from datetime import date
from utils.schedule_processor import parse_schedule_date

# Тестовые случаи: (входная строка, ожидаемый результат)
test_cases = [
    ("13 июня,", date(2024, 6, 13)),
    ("14 июня", date(2024, 6, 14)),
    ("1 мая", date(2024, 5, 1)),
    ("31 дек.", date(2024, 12, 31)),
    ("1 янв.", date(2024, 1, 1)),
    ("29 фев", date(2024, 2, 29)),
]

@pytest.mark.parametrize("input_str, expected_date", test_cases)
def test_parse_schedule_date(input_str, expected_date):
    """
    Проверяет, что функция корректно парсит разные форматы дат.
    """
    # Для тестов используем 2024 год, так как он високосный.
    assert parse_schedule_date(input_str, 2024) == expected_date

def test_parse_schedule_date_invalid():
    """
    Проверяет, что функция вызывает ошибку при некорректном вводе.
    """
    with pytest.raises(KeyError):
        parse_schedule_date("32 мартобря", 2024) 