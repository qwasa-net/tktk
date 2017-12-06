# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import Http404, redirect, render

from apps.pw.models import Board

from .models import User

logger = logging.getLogger(__name__)


def iam(rq):

    create_new = 'do_not_create' not in rq.GET

    user = User.session_user(rq, create_new=create_new)
    if not user:
        if create_new:
            raise Http404("who are you?")
        else:
            return JsonResponse({})

    whoami = {'name': user.name, 'uid': user.id}
    rq.session['uid'] = user.id
    return JsonResponse(whoami)


def there(rq):
    user = User.session_user(rq, create_new=False)
    boards = Board.objects.filter(user=user, ended_at__isnull=False).order_by('-score')[:10]
    return render(rq, 'there.html', locals())


def bye(rq):
    rq.session.flush()
    return redirect('/')
