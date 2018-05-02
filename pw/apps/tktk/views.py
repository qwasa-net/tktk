import datetime
import json
import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import authentication, exceptions, generics, serializers, response

from apps.hello.models import User
from apps.pw.models import Board, Game, Topic

logger = logging.getLogger(__name__)


class HelloUserAuth(authentication.BaseAuthentication):
    """
    user must say `hello` and get his own session before accessing the games
    """

    def authenticate(self, request):
        user = User.session_user(request, create_new=False)
        if not user:
            raise exceptions.AuthenticationFailed('who are you?')
        return (user, None)


class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name', 'description', 'lang', 'icon_url', 'engine', 'slug', 'start_url']


class TopicsListView(generics.ListAPIView):
    """
    /topics.json => list of available topics (for all engines)
    """
    authentication_classes = [HelloUserAuth, ]
    queryset = Topic.objects.filter(enabled=True).order_by('-ordering')
    serializer_class = TopicsSerializer


class BoardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class BoardGameSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(source='data_json')
    config = serializers.JSONField(source='config_json')

    class Meta:
        model = Game
        fields = ['data', 'config']


class BoardSerializer(serializers.ModelSerializer):
    user = BoardUserSerializer()
    game = BoardGameSerializer()

    class Meta:
        model = Board
        fields = ['id', 'pin', 'user', 'game']


class BoardGetView(generics.GenericAPIView):

    """
    /<topic-slug>/tktk.json => create a board for the game
    """

    authentication_classes = [HelloUserAuth, ]

    def get(self, request, *args, **kwargs):

        topic = kwargs.get("topic")
        game = Game.objects.filter(topic__slug=topic).order_by('?').first()
        if not game:
            raise Http404("no games!")

        board = Board.objects.create(
            user=request.user,
            game=game,
            pin=Board.generate_pin(request.user.name),
            started_at=datetime.datetime.now()
        )

        serializer = BoardSerializer(board)
        return response.Response(serializer.data)


class BoardSaveView(generics.GenericAPIView):

    """
    /<topic-slug>/exit => update board and exit
    """

    authentication_classes = [HelloUserAuth, ]

    def post(self, request, *args, **kwargs):

        bid = request.data.get('id')
        pin = request.data.get('pin')
        history = request.data.get('history')
        score = request.data.get('score', 0)

        board = get_object_or_404(Board, id=bid, pin=pin, user=request.user)
        board.score = score
        board.history = history
        board.ended_at = datetime.datetime.now()
        board.save()

        rsp = {'status': "OK", 'id': board.id, 'goto': "/"}
        return response.Response(rsp)
