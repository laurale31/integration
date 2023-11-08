# integration


<img width="536" alt="image" src="https://github.com/laurale31/integration/assets/85873817/1620744a-0129-49a9-8092-6d251ce3c5df">



This respository is my integration project

1. Main file: filter.py, general_filter.py
- Input: messages from a Slack channel by using Slack API to retrieve the history
- Output: A CSV file that has a value column (malicious domains), tag columns (tag_1, tag_2,...)
Main activities:
 - Extract information that contains malicious domains/URLs with their threat actors group
 - Threat actors group will be the tag of IOCs in Splunk

After extracting the data to a CSV file, I will submit the file to Splunk system.

2. retrieve_history.py
Input: messages from a Slack channel by using Slack API to retrieve the history
Output: message_history.json 
Main activities:
 - Retrieve 100 messages from the Slack channel

3. filtered_urls.csv:
- The output of the general_filter.py

4. extracted_domains.csv:
- The output of the filter.py

5. message_history.json:
- The output of the retrieve_history.py
