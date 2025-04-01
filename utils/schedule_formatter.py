"""Форматирует полученную информацию schedule_processor.py в текст для телеграм."""

import emoji

import datetime

from db_orm.crud import get_building_by_attrs
from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from tg_bot.lexicon.buttons import lexicon as btns_lexicon
from utils.schedule_processor import DayScheduleElement, ScheduleElement, ScheduleElementTiming

import locale

try:
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
except locale.Error:
    locale.setlocale(
        category=locale.LC_ALL,
        locale="ru_RU.UTF-8"
    )


class ScheduleFormatter:
    """Форматирует расписание для вывода в Telegram или текстовом виде."""

    @staticmethod
    def format_day_schedule(day_schedule: DayScheduleElement, title: str) -> str:
        """
        Форматирует расписание на день в читаемый текст.

        :param title: Название группы / имя преподавателя
        :param day_schedule: Объект расписания на день.
        :return: Отформатированное расписание.
        """

        # Заголовок с датой
        day_title = (f"{emoji.emojize(':calendar:')} Расписание на "
                     f"{day_schedule.timing.start_date.strftime('%d.%m.%y')} "
                     f"({day_schedule.timing.start_date.strftime('%A')})"
                     f"\n{title}\n")

        if not day_schedule.lessons:
            return f"{day_title}\nНа этот день занятий нет"

        formatted_lessons = []
        for lesson in day_schedule.lessons:
            formatted_lessons.append(ScheduleFormatter.format_lesson(lesson))

        return f"{day_title}\n" + "\n\n".join(formatted_lessons)

    @staticmethod
    def format_lesson(lesson: ScheduleElement) -> str:
        """
        Форматирует один элемент занятия.

        :param lesson: Объект занятия.
        :return: Отформатированная строка занятия.
        """
        # Время занятия
        time_range = f"{lesson.timing.start_date.strftime('%H:%M')}–{lesson.timing.end_date.strftime('%H:%M')}"

        # Название и тип занятия
        name_and_type = f"{lesson.name} ({lesson.type})"

        # Преподаватель
        teacher = f"{emoji.emojize(':teacher:')} <a href=\"{lesson.teacher.url}\">{lesson.teacher.name}</a>" if lesson.teacher.name \
            else f"{emoji.emojize(':teacher:')} Преподаватель не указан"

        # Аудитория
        # todo: раскоментить, когда будет готова бд
        # building = get_building_by_attrs(building_nm=lesson.auditory.name.split(",")[0])
        # building_hyper_link = f"<a href=\"https://maps.yandex.ru/{building.building_map_id}\">{lesson.auditory.name.split(',')[0]}</a>"
        building_hyper_link = lesson.auditory.name.split(',')[0]

        auditory_schedule_hyper_link = f"<a href=\"{lesson.auditory.url}\">{lesson.auditory.name.split(',')[1].strip()}</a>"

        auditory = f"{emoji.emojize(':round_pushpin:')} {building_hyper_link} {auditory_schedule_hyper_link}" if lesson.auditory.name \
            else f"{emoji.emojize(':round_pushpin:')} Место проведения не указано"

        # Ссылки
        links = ""
        if lesson.links:
            links_list = "\n".join([f"{emoji.emojize(':link:')} <a href=\"{link.url}\">{link.title}</a>"
                                    for link in lesson.links])
            links = f"\n{links_list}"

        return f"{emoji.emojize(':alarm_clock:')} {time_range} {name_and_type}\n{teacher}\n{auditory}{links}"

    @staticmethod
    def format_find_teacher_block(teacher: dict, status: str, lesson: ScheduleElement | None) -> str:
        """
        Форматирует блок с информацией о поиске локации преподавателя
        :param teacher:
        :param status: статус (None, upcoming, running)
        :param lesson:
        :return:
        """

        text = f"<b>{btns_lexicon['main_menu']['find_teacher']}</b>\n\n"
        print(text)

        if status:
            text += f"<a href=\"{lesson.teacher.url}\">{lesson.teacher.name}</a>\n\n"

            # Время занятия
            time_range = f"{lesson.timing.start_date.strftime('%H:%M')}–{lesson.timing.end_date.strftime('%H:%M')}"

            # Название и тип занятия
            name_and_type = f"{lesson.name} ({lesson.type})"

            # todo: раскоментить, когда будет готова бд
            # building = get_building_by_attrs(building_nm=lesson.auditory.name.split(",")[0])
            # building_hyper_link = f"<a href=\"https://maps.yandex.ru/{building.building_map_id}\">{lesson.auditory.name.split(',')[0]}</a>"
            building_hyper_link = lesson.auditory.name.split(',')[0]

            auditory_schedule_hyper_link = f"<a href=\"{lesson.auditory.url}\">{lesson.auditory.name.split(',')[1].strip()}</a>"

            auditory = f"{emoji.emojize(':round_pushpin:')} {building_hyper_link} {auditory_schedule_hyper_link}" if lesson.auditory.name \
                else f"{emoji.emojize(':round_pushpin:')} Место проведения не указано"

            lesson_block = f"{emoji.emojize(':alarm_clock:')} {time_range} {name_and_type}\n{auditory}"

            if status == "upcoming":
                remaining_time = (lesson.timing.start_date - datetime.datetime.now()).seconds // 60
                if remaining_time == 0:
                    remaining_time = "<1"

                text += f"У преподавателя ожидается занятие ({remaining_time} мин. до начала)\n\n"

            elif status == "running":
                remaining_time = (lesson.timing.end_date - datetime.datetime.now()).seconds // 60
                if remaining_time == 0:
                    remaining_time = "<1"

                text += f"У преподавателя идёт занятие ({remaining_time} мин. до конца)\n\n"

            text += lesson_block

        else:
            text += "У преподавателя сегодня нет занятий"
        print(text)
        return f"{text}"


if __name__ == '__main__':
    from utils.schedule_processor import get_schedule_by_date

    day_schedule_response = get_schedule_by_date(
        volume='group',
        volume_data={
            'faculty': 125,
            'group': 40518,
        },
        request_date=datetime.date(
            year=2024,
            month=11,
            day=22
        )
    )

    print(day_schedule_response)

    formatted_day_schedule = ScheduleFormatter.format_day_schedule(day_schedule_response, "Тестовый запуск")
    print(formatted_day_schedule)
