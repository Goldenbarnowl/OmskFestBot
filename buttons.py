from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# inline кнопка для проверки подписки на группу
subscription_ageree_inline_keyboard = InlineKeyboardMarkup()
subscription_ageree_inline_keyboard.add(InlineKeyboardButton(text="✅Я подписался",callback_data='agree'))

# админ меню
admin_menu_reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
winner_button = KeyboardButton(text="💡Объявить победителя")
statistik_button = KeyboardButton(text="📊Статистика")
back_button = KeyboardButton(text="⬅️Выход")
admin_menu_reply_keyboard.add(winner_button)
admin_menu_reply_keyboard.row(back_button,statistik_button)

winner_menu_keyboard = InlineKeyboardMarkup()
winner_menu_keyboard.add(InlineKeyboardButton(text="⬅️Назад",callback_data='back'))