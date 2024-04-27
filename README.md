# OmskFestBot
Телеграм бот для проверки подписки на каналы и розыгрыша

## Dependencies



- Убедитесь что у вас установлен Python версии не ниже чем 3.9.X


1. Для установки зависимостей вам необходимо прописать в консоли :

```sh
pip install -r requirements.txt
```

2. Получите все переменные для вашей среды следующим образом :

- Из документации по supabase узнайте как получить ваши SUPABASE_URL & SUPABASE_KEY

3. Теперь перейдите в @BotFather в телеграм и получите токен для вашего бота :

- Поместите токен в .env файл с параметром TOKEN 

4. Заполните файл .env по форме :
```sh
TOKEN = 'токен бота'
SUPABASE_URL = "supabase url"
SUPABASE_KEY = "supabase ключ"
CHANNEL_USERNAME = "@название канала с ботом админом"
```
5. Теперь переместите свои .env файлы в корневую директорию проекта

6. Добавьте в roles.json chat_id первого администратора

# Start 
- Пропишите в консоли следующую команду


```py
python3 main.py
```


# Documentation 

| Frame    |   Docs                                                   |
|-----------|---------------------------------------------------------|
|SupaBase   | https://supabase.com/docs |
|aiogram    | https://aiogram.readthedocs.io/_/downloads/en/latest/pdf/ |
