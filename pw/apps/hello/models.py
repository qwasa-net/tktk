# -*- coding: utf-8 -*-
import logging
import random

from django.db import models
logger = logging.getLogger(__name__)

NAME_PARTS = [
    ['жёлтый', "синий", "красный", 'белый', 'зелёный',
     "быстрый", "бодрый", "весёлый",
     'холодный', 'горячий', 'ушастый', 'хвостатый',
     'умный', 'смелый', 'храбрый', 'шустрый'],

    ["барсук", "слон", "крокодил", "воробей", "ёж",
     "жук", 'енот', 'жираф', 'суслик', 'бобёр']
]


class User(models.Model):

    name = models.CharField(max_length=100, default='anonymous')

    # timestamps
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def choose_name():
        name_parts = []
        for p in NAME_PARTS:
            np = random.choice(p)
            name_parts.append(np)
        return " ".join(name_parts)

    @classmethod
    def make_new_user(cls):
        user = cls.objects.create(name=cls.choose_name())
        return user

    @classmethod
    def session_user(cls, rq, create_new=False):

        uid = int(rq.session.get('uid', 0))
        user = None
        if uid:
            try:
                user = cls.objects.get(id=uid)
                return user
            except Exception as x:
                logger.error(x)

        if not user and create_new:
            user = cls.make_new_user()

        return user

    def __str__(self):
        return str(self.name)
