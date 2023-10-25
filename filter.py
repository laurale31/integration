import logging
import os
import csv  # Import the csv module
import re  # Import the re module for regular expressions

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
channel_id = "C4HQJJKFW"

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id)

    messages = result["messages"]

    # Extract domains with the specified formats
    extracted_domains = []

    for message in messages:
        if "text" in message:
            text = message["text"]
            # Use regular expression to extract domains in both formats from normal text
            domains = re.findall(r'storage\[\.\]googleapis\[\.\]com/[^\s]+|storage\[\.\]googleapis\[\.\]com/[^\s]+', text)
            extracted_domains.extend(domains)
            
        
        elif  "blocks" in message and message["blocks"][0]["type"] == "rich_text":
            rich_text_blocks = message["blocks"][0]["elements"]
            for block in rich_text_blocks:
                if "type" in block and block["type"] == "rich_text_preformatted":
                    preformatted_text = block.get("elements", [{}])[0].get("text")
                    if preformatted_text:
                        # Use regular expression to extract domains in both formats from preformatted text with optional "https://"
                        domains = re.findall(r'storage\[\.\]googleapis\[\.\]com/[^\s]+', preformatted_text)
                        extracted_domains.extend(domains)

    # Remove duplicates from the extracted domains
    unique_domains = list(set(extracted_domains))

    # Print results
    logger.info("{} domains found in the specified formats".format(len(unique_domains)))

    # Save extracted domains to a CSV file
    with open("extracted_domains.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Domain"])  # Write the header row
        for domain in unique_domains:
            csv_writer.writerow([domain])

    logger.info("Extracted domains saved to extracted_domains.csv")

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
