# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class ModelTS(models.Model):
    """ timestamped models (auto update_at and created_at fields) """

    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Engine(ModelTS):

    """ game engine type """
    name = models.CharField(max_length=16)
    slug = models.SlugField(max_length=16)

    def __str__(self):
        return "%s" % (self.name,)


class Topic(ModelTS):

    """ game topic """

    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=2, default=None, blank=True, null=True)
    slug = models.SlugField(max_length=16)

    icon = models.SlugField(max_length=16, blank=True, null=True)
    ordering = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.engine.name)

    @property
    def icon_url(self, ibase=settings.STATIC_URL, iext='.svg'):
        if self.icon:
            return "%s%s/%s%s" % (ibase, self.engine.slug, self.icon, iext)
        return "%s%s/icon%s" % (ibase, self.engine.slug, iext)

    @property
    def start_url(self):
        return self.slug


class Game(ModelTS):

    """ game data """

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    config = models.TextField(blank=True, null=True)
    data = models.TextField()

    def __str__(self):
        return str(self.name)


class Board(ModelTS):

    """ game + user """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    pin = models.CharField(max_length=16)

    score = models.IntegerField(default=None, null=True, blank=True)
    status = models.IntegerField(default=0)

    history = models.TextField(blank=True, null=True)

    started_at = models.DateTimeField(default=None, null=True, blank=True)
    ended_at = models.DateTimeField(default=None, null=True, blank=True)
    time2c = models.IntegerField(default=None, null=True, blank=True)

    @classmethod
    def generate_pin(klass, salt=""):
        s = "%s%i" % (salt, int(time.time()))
        return hashlib.md5(s.encode('utf8')).hexdigest()[:8]

    def __str__(self):
        return "%s %s %s %s" % (self.id, self.user.name, self.game.topic.engine.name, self.score)
