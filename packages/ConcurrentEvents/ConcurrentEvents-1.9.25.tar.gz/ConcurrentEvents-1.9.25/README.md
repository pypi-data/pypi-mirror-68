Introduction
============
``ConcurrentEvents`` is a light weight event system and threading tools build around the concurrent futures library.

The aim of this project is to create an extremely simple and generic event system as well as tools to monitor and use it effectively.

The focus of this project is based around the ``ConcurrentEvents.EventManager``, ``ConcurrentEvents.EventHandler``, ``ConcurrentEvents.Event`` classes and ``ConcurrentEvents.Catch`` decorator to create a simple and safe way to do multi-threading through an event framework.

Installation
============

[![pipeline status](https://gitlab.com/Reggles44/concurrentevents/badges/master/pipeline.svg)](https://gitlab.com/Reggles44/concurrentevents/-/commits/master)
[![coverage report](https://gitlab.com/Reggles44/concurrentevents/badges/master/coverage.svg)](https://gitlab.com/Reggles44/concurrentevents/-/commits/master)


``ConcurrentEvents`` should be installed through pip on any python version greater than ``python3.5``

.. code-block:: python

    pip install ConcurrentEvents