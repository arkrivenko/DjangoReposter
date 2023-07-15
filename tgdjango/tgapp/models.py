from django.db import models
from datetime import datetime


class User(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    active_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


def image_directory_path(instance: "Mediafile", filename: str) -> str:
    current_date = datetime.now().strftime("%d%m%Y")
    return "images/{date}/{filename}".format(
        date=current_date,
        filename=filename
    )


class ChannelData(models.Model):
    channel_login = models.CharField(null=False, max_length=40)
    description = models.TextField(blank=True, null=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.channel_login} {self.description[:30]}"


class Mediafile(models.Model):
    caption = models.TextField(null=False, max_length=1024)
    image = models.ImageField(null=False, upload_to=image_directory_path)
    description = models.TextField(blank=True, null=False, max_length=200)
    tg_groups = models.ManyToManyField(ChannelData, related_name="telegram_groups")
    task_time = models.DateTimeField(null=False, default=datetime.now())
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super(Mediafile, self).delete(*args, **kwargs)
