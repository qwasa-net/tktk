# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


class TestMe(TestCase):

    def setUp(self):
        pass

    def test_index(self):
        rsp = self.client.get('/tktk/')
        self.assertEqual(rsp.status_code, 200, "bad status_code")
        self.assertContains(rsp, "tktk")
