from django.conf.urls import url, include
from .views import GameView, TopicsListView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^(?P<topic>[a-z0-9_\-]+)/.+$', GameView.as_view(), name='tktk_game'),
    url(r'^(?P<topic>[a-z0-9_\-]+)/?$', TemplateView.as_view(template_name="tktk/game.html")),

    url(r'^topics.json$', TopicsListView.as_view(), name='tktk_game_topics_list'),
]
