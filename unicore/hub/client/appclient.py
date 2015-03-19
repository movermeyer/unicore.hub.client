from unicore.hub.client.base import (ClientException, BaseClient,
                                     BaseClientObject)


class AppClient(BaseClient):
    base_path = '/apps'

    def create_app(self, data):
        pass

    def get_app(self, app_id):
        pass

    def save_app(self, data):
        pass

    def reset_app_password(self, app_id):
        pass


class App(BaseClientObject):
    """
    A class that wraps an app's data dictionary and saves the data
    to the `unicore.hub` server.

    :param unicore.hub.client.AppClient app_client:
        A :py:class:`unicore.hub.client.AppClient` instance used to save
        and refresh the data dictionary.
    :param dict app_data:
        A dictionary containing app fields retrieved from the `unicore.hub`
        server.

    >>> app, app_password = App.create(app_client, title='Foo')
    >>> app_password
    'Bq4JlaOxXx9atOFBHpHh'
    >>> app.get('password')
    KeyError: 'password'
    >>> app.get('uuid')
    'f9e90e6b5a894c03b251df5b59c386d0'
    >>> app.get('title')
    'Foo'
    >>> app.get('groups')
    []
    >>> app.set('title', 'New Foo')
    >>> app.save()
    >>> app_password = app.reset_password()
    >>> app_password
    'BZPHmoUeQKZ2q5KHRNqb'
    >>>

    """

    @classmethod
    def create(cls, app_client, **fields):
        pass
