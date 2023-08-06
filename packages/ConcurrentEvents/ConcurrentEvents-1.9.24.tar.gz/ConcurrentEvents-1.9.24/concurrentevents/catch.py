from functools import wraps

from concurrentevents import _base
from concurrentevents.enums import Priority
from concurrentevents.event import Event


def Catch(event, priority=Priority.MEDIUM):
    """
    This is a decorator for adding member variables to a function that should be a handler of a specific event

    .. highlight:: python
    .. code-block:: python

        class ExampleHandler(EventHandler):

            @Catch(Start)
            def handleStart():
                foo()

            @Catch("Start")
            def handleStartFromString():
                bar()

            @Catch(Exit, priority=Priority.CRITICAL)
            def handleExitWithCriticalPriority():
                pass

    Args:
        :param event: Takes in a representation of an event
        :type event: str, class:`concurrentevents.Event`
    Kwargs:
        :param priority: An argument used to signal order to handlers for a specific event
        :type priority: class:`concurrentevents.Priority`, optional

    :raises TypeError: If any unaccepted values are passed in for either argument
    """

    if isinstance(event, str):
        e = event
    elif issubclass(event, Event):
        e = event.__name__
    else:
        raise TypeError(f"Catch() event argument must be an event or string, not {event}")

    try:
        p = int(priority)
    except TypeError:
        raise TypeError(f"Catch() priority argument must be convertible to an int, not {priority}")

    def decorator(f):
        f.event = e
        f.priority = p

        def unload():
            _base._handlers[e].remove(wrapper)

        f._unload = unload

        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        _base._handlers.setdefault(e, []).append(wrapper)

        return wrapper
    return decorator
