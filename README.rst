This repository has been archived
=================================

Thanks for checking out this Slack Platform code. Occasionally we archive our repos to allow us to focus on the more up to date samples. We're leaving this live as a reference.

To see the latest samples, checkout out this list - https://github.com/slackapi/sample-code-index

.. image:: https://user-images.githubusercontent.com/32463/39790649-1e029fc6-52ec-11e8-8e51-845f1f77dd58.png


Slack Pycon Workshop Bot
=============================

**This repo is to complement the live demonstration being given at Pycon 2018.**

This example app shows how easy it is to implement the Slack Events API Adapter to receive Slack Events and respond to messages using Slack's Web API via python-slackclient, with the added flair of message buttons to provide a neat feedback mechanism.

We'll be starting off with `starting-example.py`, which is a very basic echo bot based on the Slack Evants API Adapter example app available in that library's github repo. From there, we'll incrementally add additional functionality to end up in the same state as `complete-example.py`. If you're checking this out on your own, you may want to start with `complete-example.py` to see the completed [but still pretty basic] app.


🤖  Setup and running the app
------------------------------

**Set up your Python environment:**

We're using virtualenv to keep the dependencies and environmental variables specific to this app. See `virtualenv`_ docs for more info.

.. _virtualenv: https://virtualenv.pypa.io

This example app works best in Python 2.7. If 2.7 is your default version, create a virtual environment by running:

.. code::

  virtualenv env

Otherwise, if Python 3+ is your default, specify the path to your 2.7 instance:

.. code::

  virtualenv -p /your/path/to/python2 env

Then initialize the virtualenv:

.. code::

  source env/bin/activate


**Install the app's dependencies:**

.. code::

  pip install -r requirements.txt

**🤖  Create a Slack app**

Create a Slack app on https://api.slack.com/apps/

.. image:: https://cloud.githubusercontent.com/assets/32463/24877733/32979776-1de5-11e7-87d4-b5dc9e3e7973.png

**🤖  Add a bot user to your app**

.. image:: https://cloud.githubusercontent.com/assets/32463/24877750/47a16034-1de5-11e7-989b-2a90b9d8e7e3.png

**🤖  Install your app on your team**

Visit your app's **Install App** page and click **Install App to Team**.

.. image:: https://cloud.githubusercontent.com/assets/32463/24877770/61804c36-1de5-11e7-91ef-5cf2e0845729.png

Authorize your app

.. image:: https://cloud.githubusercontent.com/assets/32463/24877792/774ed94c-1de5-11e7-8857-ac8d662c5b27.png

**🤖  Save your app's credentials**

Once you've authorized your app, you'll be presented with your app's tokens.

.. image:: https://cloud.githubusercontent.com/assets/32463/24877652/d8eebbb4-1de4-11e7-8f75-2cfb1e9d45ee.png

Copy your app's **Bot User OAuth Access Token** and add it to your python environmental variables

.. code::

  export SLACK_BOT_TOKEN=xxxXXxxXXxXXxXXXXxxxX.xXxxxXxxxx

Next, go back to your app's **Basic Information** page

.. image:: https://cloud.githubusercontent.com/assets/32463/24877833/950dd53c-1de5-11e7-984f-deb26e8b9482.png

Add your app's **Verification Token** to your python environmental variables

.. code::

  export SLACK_VERIFICATION_TOKEN=xxxxxxxxXxxXxxXxXXXxxXxxx


**🤖  Start ngrok**

In order for Slack to contact your local server, you'll need to run a tunnel. We
recommend ngrok or localtunnel. We're going to use ngrok for this example.

If you don't have ngrok, `download it here`_.

.. _download it here: https://ngrok.com


Here's a rudimentary diagream of how ngrok allows Slack to connect to your server

.. image:: https://cloud.githubusercontent.com/assets/32463/25376866/940435fa-299d-11e7-9ee3-08d9427417f6.png


💡  Slack requires event requests be delivered over SSL, so you'll want to
    use the HTTPS URL provided by ngrok.

Run ngrok and copy the **HTTPS** URL

.. code::

  ngrok http 3000

.. code::

  ngrok by @inconshreveable (Ctrl+C to quit)

  Session status                      online
  Version                             2.1.18
  Region                  United States (us)
  Web Interface        http://127.0.0.1:4040

  Forwarding http://h7465j.ngrok.io -> localhost:9292
  Forwarding https://h7465j.ngrok.io -> localhost:9292

**🤖  Run the app:**

You'll need to have your server and ngrok running to complete your app's Event
Subscription setup

.. code::

  python example.py


**🤖  Subscribe your app to events**

Add your **Request URL** (your ngrok URL + ``/slack/events``) and subscribe your app to `reaction_added`, `message.channels` and `app_mentions` under bot events. **Save** and toggle **Enable Events** to `on`

.. image:: https://user-images.githubusercontent.com/1573454/30185162-644d0cb8-93ee-11e7-96af-55fe10d9d5c8.png

.. image:: https://cloud.githubusercontent.com/assets/32463/24877931/e119181a-1de5-11e7-8b0c-fcbc3419bad7.png

**🎉  Once your app has been installed and subscribed to Bot Events, you will begin receiving event data from Slack**

**👋  Interact with your bot:**

Invite your bot to a public channel, then say hi and your bot will respond

    ``hi @bot 👋``

React to your bot's greeting and the bot will echo back the eomi you reacted with

    ``@roach reacted with 😎``

Next, mention your app's bot user directly and the bot will promt you for feedback

    prompt:

    ``@bot I have feedback!``

    response:

    ``Hi @roach! How do you feel this workshop is going?``

.. image:: https://cloud.githubusercontent.com/assets/32463/23047918/964defec-f467-11e6-87c3-9c7da11fc810.gif

More neat things:
------------------
Check out the `other events you can subscribe to`_ 😎

Play with our Message Builder to see `more message formatting options`_ 😄

Browse our `example apps`_ on Github for more functionality, like Dialogs 🤩

.. _other events you can subscribe to: https://api.slack.com/events
.. _more message formatting options: https://api.slack.com/docs/messages/builder
.. _example apps: https://github.com/slackapi?utf8=%E2%9C%93&q=&type=&language=python

🤔  Support
------------

Need help? Join `Bot Developer Hangout`_ and talk to us in `#slack-api`_.

You can also `create an Issue`_ right here on GitHub.

.. _Bot Developer Hangout: http://dev4slack.xoxco.com/
.. _#slack-api: https://dev4slack.slack.com/messages/slack-api/
.. _create an Issue: https://github.com/slackapi/node-slack-events-api/issues/new
