# README for Slack URL Extractor and Categorizer

## Overview

This script is designed to extract URLs from messages in a specified Slack channel, categorize them based on predefined headings (e.g., "Fizzcore", "Celebcore", "Scam"), and save the categorized URLs to a CSV file. It utilizes the Slack SDK to interact with the Slack API and fetch message history.

## Requirements

- Python 3.x
- Required libraries:
  - `slack_sdk`
  - `python-decouple`
  - `logging`
  - `os`
  - `csv`
  - `re`

You can install the required libraries using the following command:
```bash
pip install slack_sdk python-decouple
```

## Setup

1. **Slack API Token**: Ensure you have a valid Slack API token. You can create a Slack app and generate a bot token [here](https://api.slack.com/).
2. **Environment Variables**: Store your Slack API token in an environment variable. Create a `.env` file in the root of your project and add the following line:
    ```
    SLACK_BOT_TOKEN=your_slack_bot_token
    ```
3. **Channel ID**: Replace `"CHANNEL_ID"` in the script with the actual ID of the Slack channel you want to extract URLs from.

## Usage

1. **Run the script**:
   ```bash
   python general_filter.py
   ```
   Replace `general_filter.py` with the name of your script file.

2. **Script Execution**:
   - The script will fetch the message history from the specified Slack channel.
   - It will extract URLs from the messages and categorize them based on the presence of specific keywords ("Fizzcore" or "Celebcore").
   - If no specific heading is found, the URLs will be categorized under "Scam".
   - The categorized URLs will be saved to a CSV file named `filtered_urls.csv`.

## Code Description

### Import Libraries

The script starts by importing necessary libraries:

```python
import logging
import os
import csv
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from decouple import config
```

### Initialize Slack Client and Logger

The Slack client is initialized using the bot token from environment variables, and a logger is set up:

```python
client = WebClient(token=config("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
```

### Define Channel ID

Specify the Slack channel ID from which you want to extract URLs:

```python
channel_id = "CHANNEL_ID"
```

### Fetch Messages and Extract URLs

The script fetches the message history from the specified Slack channel and processes each message to extract URLs and categorize them based on predefined headings:

```python
try:
    result = client.conversations_history(channel=channel_id)
    messages = result["messages"]

    extracted_urls = {"Fizzcore": [], "Celebcore": [], "Scam": []}

    url_pattern = r'<(https?://[^\|]+)\|'

    current_heading = None

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
                        current_heading = "Scam"
                        extracted_urls[current_heading].extend([(url, current_heading) for url in urls])

    with open("filtered_urls.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Value", "Tag_1"])

        for heading, urls in extracted_urls.items():
            for url, tag in urls:
                csv_writer.writerow([url, tag])

    logger.info("URLs extracted and tagged with the respective headings (Fizzcore, Celebcore, Scam) and saved to filtered_urls.csv")

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
```

### Error Handling

The script includes error handling to catch any exceptions raised by the Slack API:

```python
except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
```

## Output

The script generates a CSV file named `filtered_urls.csv` with the following columns:
- `Value`: The extracted URL.
- `Tag_1`: The category of the URL (e.g., "Fizzcore", "Celebcore", "Scam").

## Notes

- Ensure that the Slack API token is valid and has the necessary permissions to read messages from the specified channel.
- The script handles exceptions and logs error messages if the API call fails.

This README provides a comprehensive guide to setting up and using the script for extracting and categorizing URLs from a Slack channel.
