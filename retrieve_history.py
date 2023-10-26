import logging
import os
import json

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from decouple import config

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=config("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = "CHANNEL_ID"

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id)

    messages = result["messages"]

    # Filter out messages that have a "blocks" array and extract text content
    message_history = [
        message
        for message in messages
       
    ]

    # Print results
    logger.info("{} messages found in {}".format(len(message_history), channel_id))

    # Save filtered conversation history as a JSON file
    with open("message_history.json", "w") as json_file:
        json.dump(message_history, json_file, indent=4)

    logger.info("Filtered conversation history saved to filtered_conversation_history.json")

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
