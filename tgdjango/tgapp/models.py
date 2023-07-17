from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
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
    caption = models.TextField(null=False, max_length=1024, help_text="Подпись к посту")
    image = models.ImageField(null=False, upload_to=image_directory_path, help_text="Изображение")
    description = models.TextField(blank=True, null=False, max_length=200, help_text="Описание (в ТГ не выводится)")
    tg_groups = models.ManyToManyField(ChannelData, related_name="telegram_groups",
                                       help_text="Группы ТГ, в которых будет размещен пост")
    task_time = models.DateTimeField(null=False, default=timezone.now, help_text="Время размещения поста")
    period = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(72)],
                                 help_text="Период, с которым пост будет размещаться в ТГ")
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super(Mediafile, self).delete(*args, **kwargs)
