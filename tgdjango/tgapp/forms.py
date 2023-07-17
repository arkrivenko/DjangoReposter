from django import forms

from .models import Mediafile


class MediafileForm(forms.ModelForm):
    class Meta:
        model = Mediafile
        fields = (
            "caption",
            "image",
            "description",
            "tg_groups",
            "task_time",
            "period",
        )
