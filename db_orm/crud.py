from contextlib import contextmanager

from db_orm.models import AcademicBuilding, User, Notification, SavedSchedule
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


def get_building_by_attrs(**kwargs) -> AcademicBuilding:
    """
    Находит все корпуса по заданным значениям
    :param kwargs: id | building_nm | building_map_id
    :return:
    """
    with get_session() as session:
        query = session.query(AcademicBuilding)

        for key, value in kwargs.items():
            query = query.filter(getattr(AcademicBuilding, key) == value)

        building = query.first()
        return building


if __name__ == '__main__':
    pass
