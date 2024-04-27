from aiogram.dispatcher import FSMContext
from aiogram import types
from config import dp, bot, supabase
async def chat_history_cleaner(chat_id,message_id,state):
    try:
        data = await state.get_data()
        last_message_id = data.get('last_message_id')
        for message_id_for_delete in range(last_message_id, message_id):
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id_for_delete)
            except:
                pass
            await state.update_data(last_message_id=message_id)
    except Exception as e:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id-1)
        except:
            pass
        await state.update_data(last_message_id=message_id)