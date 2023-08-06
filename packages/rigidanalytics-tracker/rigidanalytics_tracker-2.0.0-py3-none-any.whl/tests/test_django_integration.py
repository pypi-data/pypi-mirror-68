from __future__ import print_function

import json
import os
import pytest
import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import django
from django.conf import settings
from django.test import LiveServerTestCase


@pytest.mark.usefixtures("event_handler")
class DjangoIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_django_app.settings'
        settings.MIDDLEWARE.append(
            'rigidanalytics_tracker.middleware.Analytics')
        settings.RIGID_ANALYTICS = {
            'PROJECT_ID': os.environ['RA_PROJECT_ID'],
            'PROJECT_TOKEN': os.environ['RA_PROJECT_TOKEN'],
            'DEBUG_DISABLE_ANALYTICS': False,
            'BACKEND_ENDPOINT': os.environ['RA_BACKEND_ENDPOINT'],
        }
        django.setup()
        super(DjangoIntegrationTests, cls).setUpClass()

    def test_integration(self):
        resp = requests.get(self.live_server_url)

        url = urljoin(
            os.environ['RA_BACKEND_ENDPOINT'], os.environ['RA_PROJECT_ID'])
        resp = requests.get(url)

        assert resp.ok, resp.text
        assert resp.ok
        event = resp.json()
        assert event['project_token'] == os.environ['RA_PROJECT_TOKEN'], event
        assert self.live_server_url in event['event_data']['full_url']
        assert event['event_data']['response_data']['status_code'] == 200
