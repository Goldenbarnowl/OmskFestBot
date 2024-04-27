from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from config import dp, bot, supabase, channel_username
from buttons import subscription_ageree_inline_keyboard
from state import *
from chat_history_cleaner import chat_history_cleaner
import re
from aiogram.utils.markdown import hlink

# обработка команды start

@dp.message_handler(state=User.wait_name)
async def awaitname(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.text
    data = await state.get_data()
    status = data.get('status')

    # Проверка на соответствие формату ФИО
    if re.match( r'^[А-ЯЁа-яё]+\s+[А-ЯЁа-яё]*$', name):
        telegram_name = message.from_user.username
        if telegram_name is None:
            username = "У пользователя нет имени"
        else:
            username = "@" + telegram_name
        supabase.table("UserData").insert({"chat_id": chat_id, "tg_user_name": username, "status": status, "name":name}).execute()
        await User.agree.set()
        await start_command(message,state)
    else:
        await message.reply("Пожалуйста, введите Имя и Фамилию (например, Иван Иванов)")


@dp.message_handler(content_types=types.ContentType.ANY, state="*")
async def start_command(message: types.Message, state: FSMContext):
   chat_id = message.chat.id

   # Проверяем наличие записи с таким chat_id
   query_result = supabase.from_("UserData").select("*").eq("chat_id", chat_id).execute()
   print(query_result.data)

   # Проверяем статус пользователя в канале
   chat_member = await bot.get_chat_member(channel_username, chat_id)

   if chat_member.status in ['member', 'administrator', 'creator']:
       status = True
   else:
       status = False

   if query_result.data:
      if query_result.data[0]['status'] != status:
          supabase.table('UserData').update({"status": status}).eq('chat_id', chat_id).execute()

      if status:
          message_id = await bot.send_message(chat_id, "Поздравляю, Вы участвуете в розыгрыше!🥳")
          message_id = message_id['message_id']
          await chat_history_cleaner(chat_id, message_id, state)
      else:
          await User.agree_wait.set()
          link = hlink("Cсылка *ТЫК*", "https://t.me/om_fest")
          message_id = await bot.send_message(chat_id,f"Для участия в розыгрыше, подпишитесь на этот канал. \n{link}", parse_mode = 'HTML', reply_markup=subscription_ageree_inline_keyboard )
          message_id = message_id['message_id']
          await chat_history_cleaner(chat_id, message_id, state)
   else:
       await User.wait_name.set()
       await state.update_data(status=status)
       message_id = await bot.send_message(chat_id, "Привет! \nДля участия в розыгрыше укажите Ваше имя и фамилию: ")
       message_id = message_id['message_id']
       await chat_history_cleaner(chat_id, message_id, state)


# проверка подписки на группу
@dp.callback_query_handler(lambda c: c.data == 'agree', state=User.agree_wait)
async def process_agree_callback(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id

    # Проверяем статус пользователя в канале
    chat_member = await bot.get_chat_member(channel_username, user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        try:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text="Подписка подтверждена, поздравляю, Вы участвуете в розыгрыше!🥳")
        except:
            pass
        finally:
            supabase.table('UserData').update({"status": True}).eq('chat_id', chat_id).execute()
        await User.agree.set()
    else:
        try:
            link = hlink("Cсылка *ТЫК*", "https://t.me/om_fest")
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text=f"Чтобы учавствовать в розыгрыше, надо подписаться на канал! \n{link}",parse_mode = 'HTML', reply_markup=subscription_ageree_inline_keyboard)
        except:
            pass