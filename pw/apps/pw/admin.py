# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'created_at', 'score')
    list_display_links = list_display

admin.site.register(models.Game)
admin.site.register(models.Engine)
admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.Topic)
