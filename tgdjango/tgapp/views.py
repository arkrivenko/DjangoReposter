from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Mediafile, ChannelData
from .forms import MediafileForm


class ChannelCreateView(CreateView):
    model = ChannelData
    fields = "channel_login", "description"
    success_url = reverse_lazy("tgapp:channel_list")


class ChannelListView(ListView):
    template_name = "tgapp/channel-list.html"
    context_object_name = "channels"
    queryset = ChannelData.objects.all()


class ChannelDetailView(DetailView):
    template_name = "tgapp/channel-details.html"
    model = ChannelData
    context_object_name = "channel"


class ChannelDeleteView(DeleteView):
    model = ChannelData
    success_url = reverse_lazy("tgapp:channel_list")


class MediaCreateView(CreateView):
    model = Mediafile
    fields = "caption", "image", "description", "tg_groups", "task_time", "period"
    success_url = reverse_lazy("tgapp:media_list")


class MediaUpdateView(UpdateView):
    model = Mediafile
    template_name_suffix = "_update_form"
    form_class = MediafileForm

    def get_success_url(self):
        return reverse(
            "tgapp:media_details",
            kwargs={"pk": self.object.pk},
        )


class MediaDeleteView(DeleteView):
    model = Mediafile
    success_url = reverse_lazy("tgapp:media_list")


class MediaDetailView(DetailView):
    template_name = "tgapp/media-details.html"
    model = Mediafile
    context_object_name = "media"


class MediaListView(ListView):
    template_name = "tgapp/media-list.html"
    context_object_name = "medias"
    queryset = Mediafile.objects.prefetch_related("tg_groups")
