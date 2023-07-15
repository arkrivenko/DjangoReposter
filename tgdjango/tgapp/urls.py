from django.urls import path

from .views import (
    MediaCreateView,
    MediaDeleteView,
    MediaListView,
    MediaDetailView,
    ChannelCreateView,
    ChannelDeleteView,
    ChannelListView,
    ChannelDetailView
)

app_name = "tgapp"

urlpatterns = [
    path("medias/", MediaListView.as_view(), name="media_list"),
    path("medias/create/", MediaCreateView.as_view(), name="media_create"),
    path("medias/<int:pk>/", MediaDetailView.as_view(), name="media_details"),
    path("medias/<int:pk>/delete/", MediaDeleteView.as_view(), name="media_delete"),
    path("channels/", ChannelListView.as_view(), name="channel_list"),
    path("channels/create", ChannelCreateView.as_view(), name="channel_create"),
    path("channels/<int:pk>/", ChannelDetailView.as_view(), name="channel_details"),
    path("channels/<int:pk>/delete/", ChannelDeleteView.as_view(), name="channel_delete"),
]

