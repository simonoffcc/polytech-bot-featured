from emoji import emojize
from tg_bot.lexicon.buttons import lexicon as btns_lexicon

lexicon = {
    'service': {
        'command_not_allowed': f"{emojize(':information:')} Данная команда недоступна, отправь или нажми /start",
        'reboot_ok': f"Система успешно перезагружена",
        'ruz_error': f"{emojize(':satellite_antenna:')} Не удаётся получить данные\n\nМы не можем получить данные с сервера расписания, попробуй ещё раз через несколько минут",
        'action_canceled': f"{emojize(':prohibited:')} Действие отменено"
    },
    'registration': {
        'ask_to_group': f"{emojize(':waving_hand:')} Привет! Для продолжения отправь номер своей группы\n\n<blockquote>Пример: 5130904/20102</blockquote>"
    },
    'group_updater': {
        'group_updated': f"{emojize(':information:')} <b>Данные о группе обновлены!</b>\n\nНовая группа: group_num",
        'group_inserted': f"{emojize(':information:')} <b>Данные о группе сохранены!</b>\n\nНовая группа: group_num\n\nЧтобы открыть меню, отправь или нажми /menu",
        'group_not_found': f"{emojize(':information:')} Группы с номером \"input_user_group\", попробуй ещё раз",
        'too_many_groups': f"{emojize(':information:')} Найдено слишком много групп, у которых есть \"input_user_group\" в номере. Уточни номер группы",
        'many_groups': f"{emojize(':information:')} Найдено несколько групп, у которых есть \"input_user_group\" в номере. Выбери свою",
    },
    'find_teacher': {
        'first_message': f"<b>{btns_lexicon['main_menu']['find_teacher']}</b>\n\nОтправь ФИО преподавателя или его часть, чтобы найти корпус и аудиторию, в которой находится преподаватель",
        'many_teachers': f"{emojize(':information:')} Найдено несколько преподавателей, выбери нужного",
        'too_many_teachers': f"{emojize(':information:')} Найдено слишком много преподавателей, укажи более точное ФИО",
        'teacher_not_found': f"{emojize(':information:')} Преподавателя с таким ФИО не найдено, попробуй ещё раз",
    },
    'puffins': {
        'there_is_puffins': f"{emojize(':doughnut:')} Да, пышки сегодня есть.",
        'there_is_no_puffins': f"{emojize(':doughnut:')} Нет, пышек сегодня нет.",
        'no_information': f"{emojize(':information:')} На сегодня нет информации о пышках.",
    },
    'about': {
        'info': f"{emojize(':information:')} Polytechnic class schedule chatbot with unique features.",
    }
}
