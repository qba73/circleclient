circleclient
============

.. image:: https://travis-ci.org/qba73/circleclient.svg?branch=master
    :target: https://travis-ci.org/qba73/circleclient
    
Python client library for CircleCI API.

Features
========

* Retrieving information about user
* Listing followed repositories
* Starting build
* Cancelling build
* Retrying build


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
    import circleclient
    
    
    token = os.environ['API_TOKEN']
    client = circleclient.CircleClient(api_token=token)
    
    # Retrieve User data
    info = client.user.get_info()
    print(info)
    

List projects followed by the user
----------------------------------

.. code:: python

   import os
   import circleclient
   
   
   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(api_token=token)
   
   # Retrieve information about projects
   projects = client.projects.list_projects()
   print(projects)
   

Trigger new build in CircleCI
-----------------------------

.. code:: python

   import os
   import circleclient
   
   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(api_token=token)
   
   # Trigger build
   client.build.triger_new(username='<your_username>', project='<your_project>', branch='<branch>')
   
   
Cancel running build
--------------------

.. code:: python

   import os
   import circleclient
   
   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(api_token=token)
   
   # Cancel build
   client.build.cancel(username='<your_username>', project='<your_project>', build_num=<build_number>)


Retry build
-----------

.. code:: python

   import os
   import circleclient
   
   token = os.environ['API_TOKEN']
   client = circleclient.CircleClient(api_token=token)
   
   # Rerty build
   client.build.retry(username='<your_username>', project='<your_project>', build_num=<build_number>)


