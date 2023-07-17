from django.core.management.base import BaseCommand
from django.db.models import F

from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime, timedelta

from .tg_settings import TG_TOKEN
from tgapp.models import User, Mediafile

import asyncio

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@sync_to_async
def user_get_or_create(chat_id, first_name, last_name, username):
    return list(User.objects.get_or_create(chat_id=chat_id, defaults={
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
    }))


@sync_to_async
def get_media_list():
    return list(Mediafile.objects.all())


@sync_to_async
def get_groups_list(media_pk):
    return list(Mediafile.objects.filter(pk=media_pk)[0].tg_groups.all())


@sync_to_async
def delete_media(media_pk):
    Mediafile.objects.filter(pk=media_pk).delete()


@sync_to_async
def update_task_time(media_pk):
    media = Mediafile.objects.filter(pk=media_pk)[0]
    m_task_time = media.task_time
    m_period = media.period
    Mediafile.objects.filter(pk=media_pk).update(
        task_time=(m_task_time + timedelta(hours=m_period)
                   ))
    # Mediafile.objects.filter(pk=media_pk).update(
    #     task_time=(m_task_time + timedelta(minutes=m_period)
    #                ))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user, created = await user_get_or_create(message.chat.id, message.chat.first_name,
                                             message.chat.last_name, message.chat.username)

    await message.reply(f"Привет, {user.first_name or user.username}. Я, бот!")


async def auto_sender():
    while True:
        medias = await get_media_list()
        if medias:
            for media in medias:
                task_time = datetime.strptime(media.task_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                # print(f"task time: {task_time}, time now: {datetime.now()}")
                if task_time <= datetime.now():
                    tg_groups = await get_groups_list(media_pk=media.pk)
                    for tg_group in tg_groups:
                        try:
                            photo = types.InputFile(media.image.path)
                            await bot.send_photo(tg_group.channel_login, photo=photo, caption=media.caption)
                        except Exception as ex:
                            print(ex)
                        finally:
                            continue

                    await update_task_time(media_pk=media.pk)

                    # await delete_media(media_pk=media.pk)

        await asyncio.sleep(60)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("send_data", "Отправить пост"),
        ]
    )


async def on_startup(dp):
    await set_default_commands(dp)
    await auto_sender()


class Command(BaseCommand):
    help = 'RUN COMMAND: python manage.py runbot'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
