Scott-freeze
============


Keep ``requirements.in`` with unpinned or loosely pinned requirements, and
let scott freeze them into ``requirements.txt`` for tests and deployment::

    $cat requirements.txt
    flask>0.9

::

    $ scott-freeze requirements.in > requirements.txt

::

    $ cat requirements.txt
    # Generated file. Please do not edit manually
    #
    # `requirements.in` contains direct dependencies (and may be >version instead
    # of ==version) This file is a list of dependencies and _their_ dependencies,
    # completely frozen.  To generate this file, use scott-freeze
    #
    # Example
    #     $ scott-freeze requirements.in > requirements.txt
    #
    Flask==0.10.1
    itsdangerous==0.24
    Jinja2==2.7.3
    MarkupSafe==0.23
    Werkzeug==0.9.6

