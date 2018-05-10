#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
# Slack / Pycon 2018 - Let's Build A Slack App Example App
#
# This is the started app, from here we'll add:
# - an existing Flask instance
# - a `app_mention` event handler
# - message menus
# - dynamic menu endpoints

from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

import json
import os
import urllib

# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(SLACK_BOT_TOKEN)
# ------------------------------------------------------------------------------


# ==============================================================================
# Event listened for reactions
# When a user reacts to a message, echo it to the channel
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    # Get the emoji name from the event dats
    emoji = event["reaction"]
    # Get the channel ID from the event data
    channel = event["item"]["channel"]
    user = event["user"]
    text = "<@{}> reacted with :{}:".format(user, emoji)
    slack_client.api_call("chat.postMessage", channel=channel, text=text)
# ------------------------------------------------------------------------------


# ==============================================================================
# Event listener for messages
# When subscribed to `message` events, your app will receive any messages
# sent to the channels your app has been invited to
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]

    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None:
        # If the incoming message contains "hi", then respond with a greeting
        if "hi" in message.get('text'):
            channel = message["channel"]
            message = "Hello <@{}>! :tada:".format(message["user"])
            slack_client.api_call("chat.postMessage", channel=channel, text=message)
# ------------------------------------------------------------------------------


# ==============================================================================
# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
# ------------------------------------------------------------------------------
