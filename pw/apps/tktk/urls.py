from django.conf.urls import url, include
from .views import BoardGetView, BoardSaveView, TopicsListView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^(?P<topic>[a-z0-9_\-]+)/?$', TemplateView.as_view(template_name="tktk/game.html"), name="tktk_index"),
    url(r'^(?P<topic>[a-z0-9_\-]+)/tktk.json$', BoardGetView.as_view(), name='tktk_get_game',),
    url(r'^(?P<topic>[a-z0-9_\-]+)/exit$', BoardSaveView.as_view(), name='tktk_save_game'),
    url(r'^topics.json$', TopicsListView.as_view(), name='tktk_game_topics_list'),
]
