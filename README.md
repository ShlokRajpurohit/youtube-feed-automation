# youtube-feed-automation

This Python script is a lightweight automation tool designed to fetch recent videos from a list of YouTube channels and post them to a Discord channel. It was created as a project to transition from a visual no-code platform (n8n) to a custom-scripted solution, focusing on efficiency and a deeper understanding of API integration.

### Features

- Fetches the latest videos from a configurable list of YouTube channel RSS feeds.
- Filters for new videos published within a specific timeframe (e.g., the last 24 hours).
- Excludes YouTube Shorts from the results.
- Sorts all new videos by their publication date (oldest first).
- Posts a clean, formatted message for each new video to a Discord webhook.

## Setup and Usage
Clone the Repository:
```Bash
git clone https://github.com/shlokrajpurohit/youtube-feed-automation.git
cd youtube-feed-automation
```
### Set up the Virtual Environment:
```Bash
python3 -m venv venv
source venv/bin/activate
```

### Dependencies
This script requires the Python libraries listed in requirements.txt. You can install them by running:
```Bash
pip install -r requirements.txt
```

### Configure Your Webhook and Channel IDs:
Open the main.py file.
Replace the placeholder Discord webhook URL with your own:
`DISCORD_WEBHOOK_URL = "your_discord_webhook_url_here"`
Modify the CHANNEL_IDS list with the IDs of the YouTube channels you want to monitor.

### Run the Script:
```Bash
python3 main.py
```
