import asyncio
import time

from .tg_settings import api_id, api_hash
from tgapp.models import User, Mediafile

from pyrogram import Client
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async


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
        task_time=(m_task_time + timedelta(minutes=m_period)
                   ))


async def main():
    async with app:
        while True:
            medias = await get_media_list()
            print(f"medias: {medias}")
            if medias:
                for media in medias:
                    print(f"media: {media}")
                    task_time = datetime.strptime(media.task_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                    print(f"task time: {task_time}")
                    print(f"datetime now: {datetime.now()}")
                    if task_time <= datetime.now():
                        tg_groups = await get_groups_list(media_pk=media.pk)
                        for tg_group in tg_groups:
                            print(f"tg group: {tg_group}")
                            try:
                                channel_info = await app.get_chat(tg_group.channel_login)
                                channel_id = channel_info.id
                                await app.send_photo(channel_id,
                                                     photo=media.image.path,
                                                     caption=media.caption)
                                time.sleep(5)
                            except Exception as ex:
                                print(ex)
                            finally:
                                continue

                        await update_task_time(media_pk=media.pk)
                        time.sleep(5)

            await asyncio.sleep(60)


app = Client("my_account", api_id, api_hash)
app.run(main())
