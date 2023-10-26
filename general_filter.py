import logging
import os
import csv
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from decouple import config

# Initialize the Slack API client
client = WebClient(token=config("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

# ID of the channel you want to extract URLs from
channel_id = "CHANNEL_ID"

try:
    # Call the conversations.history method using the WebClient
    result = client.conversations_history(channel=channel_id)
    messages = result["messages"]

    # Initialize dictionaries to store extracted URLs for each heading
    extracted_urls = {"Fizzcore": [], "Celebcore": [], "Scam": []}

    # Regular expression pattern to match URLs
    url_pattern = r'<(https?://[^\|]+)\|'

    current_heading = None  # Variable to keep track of the current heading

    for message in messages:
        if "text" in message:
            text = message["text"]
            lines = text.split()

            for line in lines:
                if "Fizzcore" in line:
                    current_heading = "Fizzcore"
                elif "Celebcore" in line:
                    current_heading = "Celebcore"
                else:
                    urls = re.findall(url_pattern, line)
                    if current_heading is not None:
                        extracted_urls[current_heading].extend([(url, current_heading) for url in urls])
                    else:
                        current_heading= "Scam"
                        extracted_urls[current_heading].extend([(url, current_heading) for url in urls])

    # Save the extracted URLs to a CSV file
    with open("filtered_urls.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Value", "Tag_1"])  # Write the header row

        for heading, urls in extracted_urls.items():
            for url, tag in urls:
                csv_writer.writerow([url, tag])

    logger.info("URLs extracted and tagged with the respective headings (Fizzcore or Celebcore) and saved to filtered_urls.csv")

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
