from django.shortcuts import render, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Mediafile, ChannelData


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
    fields = "caption", "image", "description", "tg_groups", "task_time"
    success_url = reverse_lazy("tgapp:media_list")


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
