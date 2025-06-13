from datetime import date
from db_orm.crud import update_puffins_status, get_puffins_status

def test_update_and_get_puffins_status(session):
    """
    Интеграционный тест:
    1. Обновляет статус пышек в тестовой БД.
    2. Получает последний статус из тестовой БД.
    3. Проверяет, что данные совпадают.
    """
    test_date = date(2024, 6, 14)
    test_message = "Пышки сегодня есть! Ура!"
    
    # 1. Обновляем статус
    update_puffins_status(session, message=test_message, is_puffins=True, target_date=test_date)
    
    # 2. Получаем статус
    latest_record = get_puffins_status(session)
    
    # 3. Проверяем
    assert latest_record is not None
    assert latest_record.date == test_date
    assert latest_record.message == test_message
    assert latest_record.is_puffins is True

def test_get_puffins_status_empty_db(session):
    """
    Проверяет, что при пустой базе функция возвращает None.
    """
    assert get_puffins_status(session) is None 