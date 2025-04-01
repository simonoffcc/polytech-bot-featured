from sqlalchemy import Column, Integer, BigInteger, Text, JSON, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AcademicBuilding(Base):
    __tablename__ = 'academic_buildings'

    id = Column(Integer, primary_key=True, comment='id корпуса')
    building_nm = Column(Text, nullable=False, comment='Название корпуса')
    building_map_id = Column(Text, nullable=False, comment='id корпуса на карте')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='Внутренний id пользователя')
    telegram_id = Column(BigInteger, unique=True, nullable=False, comment='Telegram id пользователя')
    created_at_dt = Column(DateTime, nullable=False, comment='Дата и время регистрации')
    faculty = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)
    locale = Column(Text, nullable=False, comment='Идентификатор языка')
    is_active = Column(Boolean, default=True, nullable=False, comment='Активность пользователя')

    notifications = relationship('Notification', back_populates='user', cascade='all, delete')
    saved_schedules = relationship('SavedSchedule', back_populates='user', cascade='all, delete')


class Notification(Base):
    __tablename__ = 'notifications'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True,
                     comment='Внутренний id пользователя')
    notifications_data = Column(JSON, nullable=False, comment='JSON с информацией о пушах')

    user = relationship('User', back_populates='notifications')


class SavedSchedule(Base):
    __tablename__ = 'saved_schedules'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True,
                     comment='Внутренний id пользователя')
    saved_schedules_data = Column(JSON, nullable=False, comment='JSON с информацией о расписаниях')

    user = relationship('User', back_populates='saved_schedules')

class PuffinsHistory(Base):
    __tablename__ = 'puffins_history'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='Внутренний id записи')
    date = Column(Date, nullable=False, unique=True, comment='Дата сообщения')
    message = Column(Text, nullable=False, comment='Сообщение о пышках')
    is_puffins = Column(Boolean, default=None, comment='Были ли пышки в этот день')
