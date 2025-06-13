import random
from datetime import date, timedelta
from db_orm.database import Session
from db_orm.crud import update_puffins_status

def fill_puffins_data():
    print("Заполнение базы данных тестовыми данными о пышках...")
    with Session() as session:
        today = date.today()
        for i in range(14):
            current_date = today - timedelta(days=i)
            is_available = random.choice([True, False, None])
            message = "Данные сгенерированы автоматически"
            
            # Проверяем, есть ли уже запись для этой даты
            existing_record = session.query(update_puffins_status.__globals__['PuffinsHistory']).filter_by(date=current_date).first()
            if not existing_record:
                update_puffins_status(message=message, is_puffins=is_available, target_date=current_date)
                print(f"Добавлена запись для {current_date}: {'Да' if is_available else 'Нет' if is_available is False else 'Неизвестно'}")
            else:
                print(f"Запись для {current_date} уже существует, пропуск.")

if __name__ == "__main__":
    fill_puffins_data()
    print("Готово!") 