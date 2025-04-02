from contextlib import contextmanager
from datetime import date
from sqlalchemy import desc

from db_orm.models import User, PuffinsHistory
from db_orm.database import Session


@contextmanager
def get_session():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_user(user: User) -> User:
    """
    Добавляет пользователя в базу данных
    :param user: объект класса User
    :return:
    """
    with get_session() as session:
        session.add(user)
        session.commit()

        return user


def get_user_by_attrs(**kwargs) -> User:
    """
    Находит пользователя в базе данных
    :param kwargs: id | telegram_id
    :return:
    """
    with get_session() as session:
        query = session.query(User)

        for key, value in kwargs.items():
            query = query.filter(getattr(User, key) == value)

        building = query.first()
        return building


def update_user_data(input_user: User) -> User:
    with get_session() as session:
        user = session.query(User).filter(User.id == input_user.id).first()

        user.group = input_user.group
        user.faculty = input_user.faculty
        user.is_active = input_user.is_active
        user.locale = input_user.locale

        session.commit()

    return user


def change_user_activity_status(user_id: int, status: bool) -> User:
    """
    Изменяет активность пользователя (удаление с возможностью восстановления)
    :param user_id: внутренний id пользователя
    :param status: True или False
    :return:
    """
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user.is_active != status:
            user.is_active = status
            session.commit()

        return user


def remove_user(user_id: int) -> User:
    """
    Полностью удаляет пользователя из базы данных + CASCADE ON DELETE
    :param user_id: внутренний id пользователя
    :return:
    """
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()

        return user

# ******************* Пышки *******************

def get_puffins_status(target_date: date = date.today()) -> PuffinsHistory:
    """
    Получает статус пышек за указанную дату (по умолчанию - сегодня)
    :param target_date: дата, за которую нужно получить статус
    :return: запись из PuffinsHistory
    """
    with get_session() as session:
        return session.query(PuffinsHistory).filter(PuffinsHistory.date == target_date).first()


def get_puffins_history(days: int = 14) -> list[PuffinsHistory]:
    """
    Получает историю статусов пышек за последние N дней
    :param days: количество дней для получения истории
    :return: список записей из PuffinsHistory
    """
    with get_session() as session:
        return session.query(PuffinsHistory).order_by(desc(PuffinsHistory.date)).limit(days).all()

def update_puffins_status(message: str, is_puffins: bool | None, target_date: date = date.today()) -> PuffinsHistory:
    """
    Обновляет или создает запись о статусе пышек
    :param message: текст сообщения
    :param is_puffins: статус наличия пышек (True/False/None)
    :param target_date: дата, за которую обновляется статус
    :return: обновленная или новая запись
    """
    with get_session() as session:
        existing_record = session.query(PuffinsHistory).filter(PuffinsHistory.date == target_date).first()
        
        if existing_record:
            existing_record.message = message
            existing_record.is_puffins = is_puffins
            return existing_record
        else:
            new_record = PuffinsHistory(
                date=target_date,
                message=message,
                is_puffins=is_puffins
            )
            session.add(new_record)
            return new_record


if __name__ == '__main__':
    pass
