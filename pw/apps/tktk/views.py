import datetime
import json
import logging

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.hello.models import User
from apps.pw.models import Topic, Board, Game

logger = logging.getLogger(__name__)


class TopicsListView(View):

    def get(self, rq, topic=None):

        topics = Topic.objects.filter(enabled=True).order_by('-ordering')

        data = []
        for t in topics:
            data.append({'name': t.name,
                         'description': t.description,
                         'lang': t.lang,
                         'icon_url': t.icon_url,
                         'engine': t.engine.slug,
                         'slug': t.slug,
                         'start_url': t.start_url
                         })

        return JsonResponse({'topics': data}, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class GameView(View):

    def get(self, rq, topic=None):

        user = User.session_user(rq)
        if not user:
            raise Http404("who are you?")

        game = Game.objects.filter(topic__slug=topic).order_by('?').first()

        board = Board()
        board.user = user
        board.game = game
        board.pin = board.generate_pin(user.name)
        board.started_at = datetime.datetime.now()
        board.save()

        data = {
            'id': board.id,
            'pin': board.pin,
            'user': {
                'id': user.id,
                'name': user.name
            },
            'game': {}
        }

        data['game']['data'] = json.loads(game.data)
        if game.config:
            data['game']['config'] = json.loads(game.config)

        return JsonResponse(data, content_type="application/json")

    def post(self, rq, topic=None):

        user = User.session_user(rq)
        if not user:
            raise Http404("who are you?")

        board_id = rq.POST.get('id', None)
        board_pin = rq.POST.get('pin', None)
        board_history = rq.POST.get('history', None)
        score = rq.POST.get('score', None)

        board = get_object_or_404(Board, id=board_id, pin=board_pin, user=user)
        board.score = score
        board.history = board_history
        board.ended_at = datetime.datetime.now()
        board.save()

        rsp = {'status': "OK", 'id': board.id, 'goto': "/"}

        return JsonResponse(rsp, content_type="application/json")
