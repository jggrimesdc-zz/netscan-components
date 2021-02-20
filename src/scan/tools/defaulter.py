from scan import settings


def default_kwargs_from_settings(*defaults):
    """ Defaults null keyword arguments to values in ``settings`` """

    def decorator(func):
        def wrapped(*args, **kwargs):
            for key in defaults:
                print(key)
                if kwargs.get(key) is None and hasattr(settings, key.upper()):
                    kwargs[key] = getattr(settings, key.upper(), None)
            return func(*args, **kwargs)

        return wrapped

    return decorator
