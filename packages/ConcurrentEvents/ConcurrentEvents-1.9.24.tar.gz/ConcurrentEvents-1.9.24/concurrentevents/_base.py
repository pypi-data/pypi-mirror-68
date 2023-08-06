import logging

_threads = None

_event_manager = None

# Handler Dictionary,
#   key: Event Class Name
#   value: List of function objects
_handlers = {}

_log = logging.getLogger('__main__')

_thread_monitor = {}
