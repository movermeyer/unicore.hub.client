

def client_from_config(
        client_cls, configuration, prefix='unicorehub.', **kwargs):
    settings = dict((key.lstrip(prefix), value)
                    for key, value in configuration.iteritems()
                    if key.startswith(prefix))
    settings.update(kwargs)
    return client_cls(**settings)
