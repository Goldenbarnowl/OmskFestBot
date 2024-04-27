from aiogram.utils import executor
from config import dp
from adminHendle import *
from userHundle import *
import asyncio

async def channel_checker_async():
	while True:
		try:
			print('Начинаю проверку группы')
			user_data = supabase.table("UserData").select("*").filter("status", "eq", True).execute()
			count_true_user = len(user_data.data)
			for user_count in range(count_true_user):
				# Проверяем статус пользователя в канале
				chat_member = await bot.get_chat_member(channel_username, user_data.data[user_count]['chat_id'])
				if chat_member.status in ['member', 'administrator', 'creator']:
					pass
				else:
					chat_id_deceiver = user_data.data[user_count]['chat_id']
					supabase.table('UserData').update({"status": False}).eq('chat_id', chat_id_deceiver).execute()
					await bot.send_message(chat_id_deceiver,"Похоже, что вы отписались от канала и теперь не участвуете в розыгрыше.\nЧтобы снова стать участников напишите /start ❗️❗️❗️")
			await asyncio.sleep(60)
		except:
			pass

async def on_startup(x):
	asyncio.create_task(channel_checker_async())


if __name__ == '__main__':

	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
