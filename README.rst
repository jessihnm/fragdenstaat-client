API Client for Frag Den Staat
#############################

This is a python3 project to make requests to fragdenstaat.de

Installing
==========

First install python3 then install this project as a python package:

.. code:: python

   pip install git+https://github.com/jessihnm/fragdenstaat-client@main



Usage
-----


As a python library
===================


.. code:: python

    from fragdenstaat_client.api import APIClient

    requests = client.retrieve_requests()
    print(requests)


In the terminal
===============

After installing the package a new command-line tool becomes availale in the terminal: ``fragdenstaat-client``

For now it just prints the JSON response from an API call to the public endpoint: https://fragdenstaat.de/api/v1/request/

**Example**

.. code:: bash

   fragdenstaat-client requests

