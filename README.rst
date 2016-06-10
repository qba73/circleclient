============
circleclient
============

.. image:: https://travis-ci.org/qba73/circleclient.svg?branch=master
    :target: https://travis-ci.org/qba73/circleclient
    :alt: Travis CI Build Status

.. image:: https://pypip.in/v/circleclient/badge.png
    :target: https://pypi.python.org/pypi/circleclient
    :alt: Latest Version

.. image:: https://pypip.in/license/circleclient/badge.png
    :target: https://pypi.python.org/pypi/circleclient/
    :alt: License

.. image:: https://pypip.in/d/circleclient/badge.png
    :target: https://crate.io/packages/circleclient?version=latest
    :alt: Downloads

.. image:: https://readthedocs.org/projects/circleclient/badge/?version=latest
    :target: https://readthedocs.org/projects/circleclient/?badge=latest
    :alt: Documentation Status


Python client library for CircleCI API.

Features
========

* Retrieve information about user
* List followed repositories
* Return status of recent builds for given project
* Start build
* Create parametrized builds
* List build artifacts
* Cancel build
* Retry build
* Clear build cache


Installation
============

.. code:: python

    pip install circleclient


Usage
=====

Retrieve information about User
-------------------------------

.. code:: python

    import os
    from circleclient import circleclient


    token = os.environ['API_TOKEN']
    client = circleclient.CircleClient(token)

    # Retrieve User data
    client.user.info()


List projects followed by the user
----------------------------------

.. code:: python

   import os
   from circleclient import circleclient


   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Retrieve information about projects
   client.projects.list_projects()


Trigger new build
-----------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Trigger build
   client.build.trigger('<username>', '<project_name>', '<branch>')


Trigger new parametrized build
------------------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Trigger parametrized build
   client.build.trigger('<username>', '<project_name>', '<branch>', '<PARAM1>'='<VAL1>')


Cancel running build
--------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Cancel build
   client.build.cancel('<username>', '<project_name>', '<build_number>')


Retry build
-----------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Retry build
   client.build.retry('<username>', '<project_name>', '<build_number>')


List build artifacts
--------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # List build artifacts
   client.build.artifacts('<username>', '<project_name>', '<build_number>')


Retrieve build status
---------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Retrieve build status
   client.build.status('<username>', '<project_name>', '<build_number>')


Retrieve information about builds across all projects
-----------------------------------------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Retrieve build status
   # Default limit=30, offset=0
   client.build.recent_all_projects(limit=<int>, offset=0)
   client.build.recent_all_projects()


Retrieve information about recent build(s)
------------------------------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Retrieve build status
   # Default limit=30, offset=0, branch=None
   client.build.recent('<username>', '<project>', limit='<int>', offset='<int>')

   # Retrieve last 10 builds of branch master
   client.build.recent('<username>', '<project>', limit=10, branch='master')

   # Retrieve last build of branch develop
   client.build.recent('<username>', '<project>', branch='develop')


Retrieve filtered information about recent build(s)
---------------------------------------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(token)

   # Retrieve build status and filter results
   client.build.recent('<username>',
                       '<project>',
                       branch='master',
                       status_filter='completed')

   client.build.recent('<username>',
                       '<project>',
                       branch='develop',
                       status_filter='successful')

   client.build.recent('<username>',
                       '<project>',
                       limit=10,
                       status_filter='failed')

   client.build.recent('<username>',
                       '<project>',
                       status_filter='running') 


Clear build cache
-----------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(api_token=token)

   # Clear build cache
   client.cache.clear(username='<username>', project='<project_name>')


Use a custom CircleCI endpoint
------------------------------

.. code:: python

   import os
   from circleclient import circleclient

   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(api_token=token, endpoint='https://cci.example.com/api/v1')

   # Use client as normal
   client.user.info()
