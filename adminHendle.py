from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from config import dp, bot, supabase, channel_username
from buttons import admin_menu_reply_keyboard, winner_menu_keyboard
from state import *
from chat_history_cleaner import chat_history_cleaner
import json
from aiogram.types import ReplyKeyboardRemove
from generate_random import generate_random_numbers

@dp.message_handler(commands=['admin'], state='*')
async def admin_command(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # Проверка, что пользователь в списке админов
    with open('roles.json') as f:
        admin_roles = json.load(f)['admins']

    if str(message.from_user.id) in admin_roles:
        # Установка состояния и вывод кнопок админки
        await Admin.menu.set()
        message_id = await bot.send_message(chat_id,"Вы вошли в панель администратора", reply_markup=admin_menu_reply_keyboard)
        message_id = message_id['message_id']
        await chat_history_cleaner(chat_id, message_id, state)
    else:
        message_id = await bot.send_message(chat_id,"У вас нет прав администратора!")
        message_id = message_id['message_id']
        await chat_history_cleaner(chat_id, message_id, state)

@dp.message_handler(commands=['give_root'], state=Admin.menu)
async def give_root(message: types.Message):
    if len(message.text.split()) == 2:
        admin_name = message.text.split()[1]
        try:
            admin_name = supabase.from_("UserData").select("chat_id").eq("tg_user_name", admin_name).execute()
            admin_name = admin_name.data[0]['chat_id']
            with open('roles.json', 'r+') as f:
                data = json.load(f)
                if "новое_число" not in data['admins']:
                    data['admins'].append(str(admin_name))
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    await message.reply("Пользователь теперь администратор")
                else:
                    await message.reply("Этот пользователь уже является администратором")
        except Exception as e:
            await message.reply("Человек должен быть зарегистрирован в боте\nКод ошибки: " + str(e))


@dp.message_handler(commands=['delete_root'], state=Admin.menu)
async def delete_root(message: types.Message):
    if len(message.text.split()) == 2:
        admin_name = message.text.split()[1]
        try:
            admin_name = supabase.from_("UserData").select("chat_id").eq("tg_user_name", admin_name).execute()
            admin_name = str(admin_name.data[0]['chat_id'])
            with open('roles.json', 'r+') as f:
                data = json.load(f)
                if admin_name in data['admins']:
                    data['admins'].remove(admin_name)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    await message.reply("Пользователь теперь НЕ администратор")
                else:
                    await message.reply("Этот пользователь не является администратором")
        except Exception as e:
            await message.reply("Человек должен быть зарегистрирован в боте\nКод ошибки: " + str(e))

@dp.message_handler(text="💡Объявить победителя", state=Admin.menu)
async def winner_search(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_data = supabase.table("UserData").select("*").filter("status", "eq", True).execute()
    count_true_user = len(user_data.data)
    for user_count in range(count_true_user):
        # Проверяем статус пользователя в канале
        chat_member = await bot.get_chat_member(channel_username, user_data.data[user_count]['chat_id'])
        if chat_member.status in ['member', 'administrator', 'creator']:
            pass
        else:
            count_true_user-=1
            supabase.table('UserData').update({"status": False}).eq('chat_id', user_data.data[user_count]['chat_id']).execute()
    await Admin.wait_winner_count.set()
    message_id = await bot.send_message(chat_id, "Введите количество победителей \nОт 1 до " + str(count_true_user),reply_markup=winner_menu_keyboard)
    message_id = message_id['message_id']
    await chat_history_cleaner(chat_id, message_id, state)

@dp.message_handler(state=Admin.wait_winner_count)
async def wait_count_winners(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_data = supabase.table("UserData").select("*").filter("status", "eq", True).execute()
    count_true_user = len(user_data.data)
    try:
        count = int(message.text)
        winners_list = generate_random_numbers(0, count_true_user-1, count)
        winners = ""
        print(winners_list)
        for winners_number in winners_list:
            # Проверяем статус пользователя в канале
            chat_member = await bot.get_chat_member(channel_username, user_data.data[winners_number]['chat_id'])
            if chat_member.status in ['member', 'administrator', 'creator']:
                winners += f'\n{user_data.data[winners_number]["tg_user_name"]} - {user_data.data[winners_number]["name"]}'
                print(winners)
            else:
                print('Пользователь ' + str(user_data.data[winners_number]['tg_user_name'])+ ' отписался от группы, начинаю поиск замены')
        await Admin.menu.set()
        message_id = await bot.send_message(chat_id, winners, reply_markup=admin_menu_reply_keyboard)
        message_id = message_id['message_id']
        await chat_history_cleaner(chat_id, message_id, state)
    except Exception as e:
        await Admin.wait_winner_count.set()
        message_id = await bot.send_message(chat_id, f"Введите количество победителей, это должно быть ЦЕЛОЕ число, в диапазоне от 1 до {str(count_true_user)}\nКод ошибки {str(e)}",reply_markup=winner_menu_keyboard)
        message_id = message_id['message_id']
        await chat_history_cleaner(chat_id, message_id, state)

@dp.callback_query_handler(lambda c: c.data == 'back', state=Admin.wait_winner_count)
async def back_admin_menu_Inline(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    await Admin.menu.set()
    message_id = await bot.send_message(chat_id, "Вы вошли в панель администратора",reply_markup=admin_menu_reply_keyboard)
    message_id = message_id['message_id']
    await chat_history_cleaner(chat_id, message_id, state)


@dp.message_handler(text="📊Статистика", state=Admin.menu)
async def statistik(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # Получаем количество всех пользователей
    data = supabase.table("UserData").select("chat_id").execute()
    all_users = len(data.data)

    # Получаем количество пользователей, подписанных на группу
    data = supabase.table("UserData").select("*").filter("status", "eq", True).execute()
    user_status_true = len(data.data)
    print(data.data)
    text = "📊Статистика \n Количество пользователей: " + str(all_users) + "\n Количество подписанных на группу: " + str(user_status_true)
    await bot.send_message(chat_id, text, reply_markup=admin_menu_reply_keyboard)


@dp.message_handler(text="⬅️Выход", state=Admin.menu)
async def back_from_admin_panel(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    message_id = await bot.send_message(chat_id, "Вы вышли из панели администратора", reply_markup=ReplyKeyboardRemove())
    message_id = message_id['message_id']
    await chat_history_cleaner(chat_id, message_id, state)
    await User.agree.set()