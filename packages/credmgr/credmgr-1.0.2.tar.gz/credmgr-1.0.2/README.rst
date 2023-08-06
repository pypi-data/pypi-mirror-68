CredentialManager
=================

Client for interacting with Credential Manager API

-  API version: 1.0
-  Package version: 1.0.1

Requirements
------------

Python 3.6+

Installation & Usage
--------------------

.. code:: sh

    pip install credmgr

Then import the package:

.. code:: python

    import CredentialManager

Getting Started
---------------

.. code:: python

    import CredentialManager

    credmgr = CredentialManager.client(api_token='apiToken')

    # List all Reddit apps
    redditApps = credmgr.reddit_apps()
    for redditApp in redditApps:
        print(redditApp.app_name)

    # Create a Reddit app
    redditApp = credmgr.reddit_app.create(app_name='redditAppName', client_id='client_id', client_secret='client_secret', user_agent='user_agent', redirect_uri='redirect_uri')

    # Get the app by id
    redditApp = credmgr.reddit_app(1)

    # Edit the Reddit app
    redditApp.edit(client_id='new Client_id')

    # Delete the app
    redditApp.delete()