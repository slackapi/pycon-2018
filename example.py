# ==============================================================================
# Slack / Pycon 2018 - Let's Build A Slack App Example App

from flask import Flask, request, make_response, Response
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

import json
import os
import urllib

# This is the Flask instance that our event handler will be bound to
# If you don't have an existing Flask app, the events api adapter
# will instantiate it's own Flask instance for you
app = Flask(__name__)

# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events", app)

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
CLIENT = SlackClient(SLACK_BOT_TOKEN)
# ------------------------------------------------------------------------------


# ==============================================================================
# Helper to send a message asking how the workshop is going, with a select menu
def send_survey(user, channel):
    # A Dictionary of message attachment options
    # More info: https://api.slack.com/docs/message-menus
    attachments_json = [
        {
            "fallback": "Upgrade your Slack client to use messages like these.",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "menu_options",
            "actions": [
                {
                    "name": "option_list",
                    "text": "Pick an option...",
                    "type": "select",
                    # Load the menu options from an external source
                    # served from the message_options endpoint below
                    "data_source": "external"
                }
            ]
        }
    ]

    # Send an in-channel reply to the user, asking for feedback
    CLIENT.api_call(
      "chat.postMessage",
      channel=channel,
      text="Hi <@{}>! How do you feel this workshop is going?".format(user),
      attachments=attachments_json
    )
# ------------------------------------------------------------------------------


# ==============================================================================
# The endpoint Slack will load your menu options from
@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    if SLACK_VERIFICATION_TOKEN != form_json["token"]:
        raise("Invalid Verification Token")

    # Dictionary of menu options which will be sent as JSON
    menu_options = {
        "options": [
            {
                "text": "Great",
                "value": "great"
            },
            {
                "text": "Not so great",
                "value": "no_so_great"
            }
        ]
    }

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')
# ------------------------------------------------------------------------------


# ==============================================================================
# When a user selects from the message menu, Slack sends the response here
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    if SLACK_VERIFICATION_TOKEN != form_json["token"]:
        raise("Invalid Verification Token")

    # Get the user's selection from the action payload
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    # Check the user's menu selection and set the correct message
    if selection == "great":
        message_text = "I'm glad to hear this workshop is going great!"
        tweet_text = "This #Pycon2018Slack app workshop is going great!"
    else:
        message_text = "Oh no! Please let Roach know you're having trouble :cry:"
        tweet_text = "I'm learning how to build bots at #Pycon2018Slack!"

    # Escape the Tweet text content, since it's passed as a query param
    encoded_text = urllib.quote_plus(tweet_text)
    tweet_url = "https://twitter.com/intent/tweet?text={}".format(encoded_text)

    # The link button is a powerful and often overlooked message action elements
    link_button = [{
        "fallback": "Upgrade your Slack client to use message buttons",
        "actions": [
            {
                "type": "button",
                "text": ":bird: Tweet about it!",
                "url": tweet_url
            }
        ]
    }]

    # Update the bot's message to reflect the user's selection
    CLIENT.api_call(
      "chat.update",
      # The Channel in which the original message was posted
      channel=form_json["channel"]["id"],
      # The original message's timestamp/ID
      ts=form_json["message_ts"],
      text=message_text,
      attachments=link_button
    )

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)
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
    text = ":{}:".format(emoji)
    CLIENT.api_call("chat.postMessage", channel=channel, text=text)
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
            CLIENT.api_call("chat.postMessage", channel=channel, text=message)
# ------------------------------------------------------------------------------


# ==============================================================================
# Event listener for app_mention events
# app_mention events allow you to subscribe to only the messages directed
# at your app's bot user
@slack_events_adapter.on("app_mention")
def handle_app_mention(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None:
        # If the incoming message contains "hi", then respond with
        # a "Hello" message
        if "feedback" in message.get('text'):
            send_survey(message["user"], message["channel"])
# ------------------------------------------------------------------------------


# ==============================================================================
# Start the Flask server on port 3000
if __name__ == "__main__":
    app.run(port=3000)
# ------------------------------------------------------------------------------
