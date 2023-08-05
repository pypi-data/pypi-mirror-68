#Introduction

``Products.BeakerZopeSessionManager`` is a replacement for the default Zope 4
session implementation.  It uses [Beaker][1] as a backend (via [collective.beaker][2])
and adapts the Beaker session to provide the same interface as a normal Zope
session.

Beaker is a better alternative to the default session implementation for several
reasons:

 * The Zope session implementation does not perform well in high-write scenarios.
 * Beaker provides better flexibility in where session data is actually stored.
 * Beaker is used and maintained outside of the Zope ecosystem.

.. Note::
   If you are developing a product that needs sessions but are not already
   using Zope sessions, you should probably just use collective.beaker
   directly. This product is meant for use with existing add-ons that already
   use Zope sessions (i.e. request.SESSION).

#Installation

Include the line ``<include package="collective.beaker" />`` in yout site.zcml

Edit the file ``lib/python3.7/site-packages/Zope2/Startup/serve.py`` inside your virtual env.

Replace (line 200):
```python
try:
    serve(app)`
except (SystemExit, KeyboardInterrupt) as e:
```
with:
```python
try:
    from beaker.middleware import SessionMiddleware
    config = {
        'session.type': 'file',
        'session.auto': True,
        'session.save_accessed_time': True,
        'session.data_dir': '/tmp/sessions/data',
        'session.lock_dir': '/tmp/sessions/lock',
        'session.timeout': 28800
    }
    server(SessionMiddleware(app, config))
except (SystemExit, KeyboardInterrupt) as e:
```
For more info on how to configure your Beaker, please refer to [Beaker][1] documentation.

#Notes

* Beaker does not automatically clean up old sessions, so you may want to set
  up a cron job to take care of this.

#Contributors

* Gabriel Gisoldo [gabrielgisoldo]

.. include:: CHANGES.rst

[1]: http://https://beaker.readthedocs.io/en/latest/index.html "Beaker"
[2]: http://pypi.python.org/pypi/collective.beaker "collective.beaker"
