from contextlib import contextmanager
from datetime import date, datetime, timedelta
from sqlalchemy import desc
from sqlalchemy.orm import Session as SessionType

from db_orm.models import User, PuffinsHistory, Notification, SavedSchedule
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


def create_user(session: SessionType, telegram_id, faculty, group, locale='ru') -> User:
    """
    Добавляет пользователя в базу данных
    :param session: сессия SQLAlchemy
    :param telegram_id: ID пользователя в Telegram
    :param faculty: факультет пользователя
    :param group: группа пользователя
    :param locale: язык пользователя
    :return: созданный пользователь
    """
    new_user = User(
        telegram_id=telegram_id,
        created_at_dt=datetime.now(),
        faculty=faculty,
        group=group,
        locale=locale,
        is_active=True
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_attrs(session: SessionType, telegram_id: int | None = None, user_id: int | None = None) -> User | None:
    """
    Находит пользователя в базе данных
    :param session: сессия SQLAlchemy
    :param telegram_id: ID пользователя в Telegram
    :param user_id: внутренний ID пользователя
    :return: найденный пользователь или None
    """
    if telegram_id:
        return session.query(User).filter(User.telegram_id == telegram_id).first()
    elif user_id:
        return session.query(User).filter(User.id == user_id).first()
    return None


def update_user_data(session: SessionType, telegram_id, **kwargs):
    """
    Обновляет данные пользователя в базе данных
    :param session: сессия SQLAlchemy
    :param telegram_id: ID пользователя в Telegram
    :param kwargs: ключи и значения для обновления
    :return: обновленный пользователь или None
    """
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
        return user
    return None


def change_user_activity_status(session: SessionType, user_id: int, status: bool) -> User:
    """
    Изменяет активность пользователя (удаление с возможностью восстановления)
    :param session: сессия SQLAlchemy
    :param user_id: внутренний ID пользователя
    :param status: True или False
    :return: обновленный пользователь
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user.is_active != status:
        user.is_active = status
        session.commit()
    return user


def remove_user(session: SessionType, user_id: int) -> User:
    """
    Полностью удаляет пользователя из базы данных + CASCADE ON DELETE
    :param session: сессия SQLAlchemy
    :param user_id: внутренний ID пользователя
    :return: удаленный пользователь
    """
    user = session.query(User).filter(User.id == user_id).first()
    session.delete(user)
    session.commit()
    return user

# ******************* Пышки *******************

def get_puffins_status(session: SessionType) -> PuffinsHistory | None:
    """
    Получает статус пышек за последнюю дату
    :param session: сессия SQLAlchemy
    :return: запись из PuffinsHistory или None
    """
    return session.query(PuffinsHistory).order_by(desc(PuffinsHistory.date)).first()


def get_puffins_history(session: SessionType, days: int = 14) -> list[PuffinsHistory]:
    """
    Получает историю статусов пышек за последние N дней
    :param session: сессия SQLAlchemy
    :param days: количество дней для получения истории
    :return: список записей из PuffinsHistory
    """
    return session.query(PuffinsHistory).order_by(desc(PuffinsHistory.date)).limit(days).all()


def get_puffins_history_last_two_weeks(session: SessionType):
    """
    Получает историю статусов пышек за последние две недели
    :param session: сессия SQLAlchemy
    :return: список записей из PuffinsHistory
    """
    two_weeks_ago = datetime.now() - timedelta(days=14)
    return session.query(PuffinsHistory).filter(PuffinsHistory.date >= two_weeks_ago.date()).order_by(PuffinsHistory.date.asc()).all()


def update_puffins_status(session: SessionType, message: str, is_puffins: bool | None, target_date: date = date.today()) -> PuffinsHistory:
    """
    Обновляет или создает запись о статусе пышек
    :param session: сессия SQLAlchemy
    :param message: текст сообщения
    :param is_puffins: статус наличия пышек (True/False/None)
    :param target_date: дата, за которую обновляется статус
    :return: обновленная или новая запись
    """
    existing_record = session.query(PuffinsHistory).filter_by(date=target_date).first()
    
    if existing_record:
        existing_record.message = message
        existing_record.is_puffins = is_puffins
        record = existing_record
    else:
        new_record = PuffinsHistory(
            date=target_date,
            message=message,
            is_puffins=is_puffins
        )
        session.add(new_record)
        record = new_record

    session.commit()
    session.refresh(record)
    return record


if __name__ == '__main__':
    pass
