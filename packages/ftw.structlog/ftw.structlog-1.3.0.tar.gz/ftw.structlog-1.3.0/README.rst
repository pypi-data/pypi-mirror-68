ftw.structlog
=============

This package implements **structured request logging in Plone**.

It does so by writing logfiles (one per instance) that contain one JSON entry
per line for every request. That JSON entry contains all the information the
Z2 log provides, and more, in structured key/value pairs.


Installation
------------

- Install ``ftw.structlog`` by adding it to the list of eggs in your buildout.
  Then run buildout and restart your instance:

.. code:: ini

    [instance]
    eggs +=
        ftw.structlog

- Alternatively, add it as a dependency to your package's ``setup.py``.


Logged Information
------------------

Example entry:

.. code:: json

    {
      "bytes": 6875,
      "cient_ip": "127.0.0.1",
      "duration": 0.30268411636353,
      "host": "127.0.0.1",
      "method": "GET",
      "referer": "http:\/\/localhost:8080\/plone",
      "site": "plone",
      "status": 200,
      "timestamp": "2017-07-29T12:30:58.000750+02:00",
      "url": "http:\/\/localhost:8080\/plone\/my-page",
      "user": "john.doe",
      "user_agent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/60.0.3112.113 Safari\/537.36",
      "view": "some_view"
    }


The logged JSON entry contains the following data:

+------------+---------------------------------------------------------------+
| key        | value                                                         |
+============+===============================================================+
| bytes      | Size of response body in bytes (``Content-Length``)           |
+------------+---------------------------------------------------------------+
| client_ip  | Host where the request originated from (respecting            |
|            | X-Forwarded-For)                                              |
+------------+---------------------------------------------------------------+
| duration   | Time spent in ZPublisher to handle request (time between      |
|            | ``IPubStart`` and ``IPubSuccess`` / ``IPubFailure`` )         |
+------------+---------------------------------------------------------------+
| host       | Deprecated. You should use ``client_ip`` instead.             |
+------------+---------------------------------------------------------------+
| method     | HTTP request method                                           |
+------------+---------------------------------------------------------------+
| referer    | Referer                                                       |
+------------+---------------------------------------------------------------+
| site       | Plone site ID                                                 |
+------------+---------------------------------------------------------------+
| status     | HTTP response status                                          |
+------------+---------------------------------------------------------------+
| timestamp  | Time when request was received (non-naive local time in ISO   |
|            | 8601, in the server's local timezone as determined by         |
|            | ``tzlocal``)                                                  |
+------------+---------------------------------------------------------------+
| url        | URL of the request (including query string if present)        |
+------------+---------------------------------------------------------------+
| user       | Username of the authenticated user, ``"Anonymous"`` otherwise |
+------------+---------------------------------------------------------------+
| user_agent | User-Agent                                                    |
+------------+---------------------------------------------------------------+
| view       | Name of the browser view or REST API endpoint  (see below)    |
+------------+---------------------------------------------------------------+


If ``SQLAlchemy`` is installed and integrated via ``z3c.saconfig``, SQL query
times will also be logged. For requests that perform SQL queries, there will
be an additional key ``sql_query_time`` containing the cumulative time of
all SQL queries during that request:

+----------------+----------------------------------------------------------------+
| key            | value                                                          |
+================+================================================================+
| sql_query_time | Cumulative time of all SQL queries during request (in seconds) |
+----------------+----------------------------------------------------------------+


Logfile Location
----------------

One logfile per Zope2 instance will be created, and its location and name
will be derived from the instance's eventlog path. If the instance's eventlog
path is ``var/log/instance2.log``, the JSON logfile's path will be
``var/log/instance2-json.log``.

**Note**: Because ``ftw.structlog`` derives its logfile name from the
eventlog path, an eventlog *must* be configured in ``zope.conf``, otherwise
``ftw.structlog`` will not log any requests and complain noisily through
the root logger.

When running tests in other projects, these errors can be muted by setting the
environment variable ``FTW_STRUCTLOG_MUTE_SETUP_ERRORS=true``.

View Name
---------

An attempt is made to log the name of the invoked browser view or REST API
endpoint, so that requests to particular views can easily be grouped without
having to resort to URL string parsing.

However, this is intentionally limited, and aims to only handle the most
common and useful cases. It's also implemented in a way to not fill up logs
with too many diverse values for ``view``, by grouping together very
common requests (CSS and JS assets) under common names.

The following table gives an example of how names of different "views" are
logged:

+-------------------------------------------------+----------------------+
| View Type                                       | view                 |
+=================================================+======================+
| Regular browser view                            | 'some_view'          |
+-------------------------------------------------+----------------------+
| Regular browser view, published attributes      | 'some_view/attr'     |
+-------------------------------------------------+----------------------+
| plone.rest named services                       | '@actions'           |
+-------------------------------------------------+----------------------+
| plone.rest named services with path params      | '@users'             |
+-------------------------------------------------+----------------------+
| plone.rest unnamed GET/POST/...                 | 'context'            |
+-------------------------------------------------+----------------------+
| CSS                                             | 'portal_css'         |
+-------------------------------------------------+----------------------+
| JS                                              | 'portal_javascripts' |
+-------------------------------------------------+----------------------+
| Resources                                       | '++resource++'       |
+-------------------------------------------------+----------------------+
| Theme resources                                 | '++theme++'          |
+-------------------------------------------------+----------------------+


Links
-----

- Github: https://github.com/4teamwork/ftw.structlog
- Issues: https://github.com/4teamwork/ftw.structlog/issues
- Pypi: http://pypi.python.org/pypi/ftw.structlog
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.structlog


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.structlog`` is licensed under GNU General Public License, version 2.
