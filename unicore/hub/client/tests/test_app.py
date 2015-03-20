from unittest import TestCase
from uuid import uuid4

import mock

from unicore.hub.client import App


class AppTestCase(TestCase):
    app_data = {
        'uuid': uuid4().hex,
        'title': 'Foo',
        'groups': ['group:apps_manager']
    }

    def create_app(self, app_client=None, **data_overrides):
        data = self.app_data.copy()
        data.update(data_overrides)

        if not app_client:
            app_client = mock.Mock()

        return App(app_client, data)

    def test_set(self):
        app = self.create_app()

        # check that immutable fields cannot be set
        for field in ('uuid', 'password'):
            with self.assertRaisesRegexp(ValueError, 'cannot be set'):
                app.set(field, 'new_%s' % field)

        # check that other fields can be set
        app.set('title', 'New Foo')
        self.assertEqual(app.data['title'], 'New Foo')

    def test_get(self):
        app = self.create_app()

        with self.assertRaises(KeyError):
            app.get('doesnotexist')

        self.assertEqual(self.app_data['title'], app.get('title'))

    def test_save(self):
        app = self.create_app()
        app.save()

        app.client.save_app_data.assert_called_with(
            self.app_data['uuid'], self.app_data)

    def test_refresh(self):
        app = self.create_app()
        new_app_data = {
            'uuid': self.app_data['uuid'],
            'title': 'New Foo',
            'groups': [],
        }
        self.assertNotEqual(app.data, new_app_data)

        app.client.get_app_data = mock.Mock()
        app.client.get_app_data.return_value = new_app_data
        app.refresh()
        app.client.get_app_data.assert_called_with(self.app_data['uuid'])
        self.assertEqual(app.data, new_app_data)

    def test_reset_password(self):
        app = self.create_app()
        app.client.reset_app_password = mock.Mock()
        app.client.reset_app_password.return_value = 'new_password'

        password = app.reset_password()
        app.client.reset_app_password.assert_called_with(self.app_data['uuid'])
        self.assertEqual(password, 'new_password')
        self.assertNotIn('password', app.data)
