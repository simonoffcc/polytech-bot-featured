from emoji import emojize

lexicon = {
    'service': {
      'cancel_action': f"{emojize(':prohibited:')} Отменить"
    },
    'main_menu': {
        'main_menu': f"{emojize(':card_file_box:')} Главное меню",
        'today_schedule': f"{emojize(':calendar:')} Расписание на сегодня",
        'week_schedule': f"{emojize(':calendar:')} Расписание на неделю",
        'export_today': f"{emojize(':inbox_tray:')} Экспорт на сегодня",
        'export_week': f"{emojize(':inbox_tray:')} Экспорт на неделю",
        'puffins': f"{emojize(':doughnut:')} Есть ли пышки?",
        'about': f"{emojize(':information:')} О боте",
        'find_teacher': f"{emojize(':teacher:')} Где препод?",
        'buildings': f"{emojize(':school:')} Корпуса",
        'webapp': f"📲 Вебапп",
    }
}
