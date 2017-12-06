# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


class TestHello(TestCase):

    def setUp(self):
        pass

    def test_noone(self):
        rsp = self.client.get('/hello/__whoami?')  # , HTTP_HOST='docs.djangoproject.dev:8000')
        self.assertEqual(rsp.status_code, 200, "bad status_code: %i" % (rsp.status_code))
        who = rsp.json()
        self.assertIn('name', who, "Name in /hello/")

    def test_me(self):
        pass
