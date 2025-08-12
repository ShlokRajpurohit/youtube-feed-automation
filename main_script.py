
# This script automates fetching recent YouTube videos from a list of channels
# and posting them to a Discord channel via a webhook.

# Dependencies:
# - requests
# - feedparser

import requests
import feedparser
import time
from datetime import datetime, timedelta

# --- Configuration ---
# Your Discord webhook URL goes here.
DISCORD_WEBHOOK_URL = "your_discord_webhook_url_here"

# A list of YouTube channel IDs to monitor.
CHANNEL_IDS = ["UCZXW8E1__d5tZb-wLFOt8TQ", "UCSUf5_EPEfl4zlBKZHkZdmw", "UCMr1lqB1oN3-cYf6cj6-v-A", "UCU2fTtyIj4uJ0uYlQnEH3LA", "UCU2fTtyIj4uJ0uYlQnEH3LA", "UCXuqSBlHAE6Xw-yeJA0Tunw", "UCCC4-ZHzMHUKNyDENY7Pk6Q", "UC-lHJZR3Gqxm24_Vd_AJ5Yw", "UCzgCuuPQa1nMlZP9ruPYDNw", "UCfogw3upPjt7ht4d3DpMSHw", "UCwxJalZcDrdG_IMdTE5IIhw"]


def send_to_discord(webhook_url, message_content):
    """
    Sends a message to a Discord webhook.

    Args:
        webhook_url (str): The URL of the Discord webhook.
        message_content (str): The content of the message to send.
    
    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    payload = {
        "content": message_content
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        # Raise an exception for bad status codes
        response.raise_for_status() 
        print("Message sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Discord: {e}")
        return False


def main(yt_ids, minutes_ago=1):
    """
    Main function to orchestrate the video fetching, filtering, and posting workflow.

    Args:
        yt_ids (list): A list of YouTube channel IDs.
        minutes_ago (int): The number of minutes to look back for new videos.
    """
    all_videos = []
    
    # Calculate the cutoff date for recent videos using local time.
    one_day_ago = datetime.now() - timedelta(minutes=minutes_ago)

    # STEP 1: GATHER ALL VIDEOS FROM ALL CHANNELS
    for channel_id in yt_ids:
        try:
            feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            r = requests.get(feed_url, timeout=10)
            r.raise_for_status()
            parsed_feed = feedparser.parse(r.content)
            
            for video in parsed_feed.entries:
                # Convert the published date from the feed into a timezone-naive datetime object.
                video_published_datetime = datetime.fromtimestamp(time.mktime(video.published_parsed))

                # Filter for videos published after the cutoff date and exclude Shorts.
                if video_published_datetime >= one_day_ago and "/shorts/" not in video.link:
                    # Store the video object and its datetime object together.
                    all_videos.append({
                        'video_obj': video,
                        'published_dt': video_published_datetime
                    })
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching feed for channel {channel_id}: {e}")
            continue

    # STEP 2: SORT THE SINGLE LIST BY PUBLISHED DATE
    # Sort the list of dictionaries based on the 'published_dt' key.
    all_videos.sort(key=lambda x: x['published_dt'])

    # STEP 3: PROCESS THE FINAL, SORTED LIST
    if not all_videos:
        print(f"No new videos found in the last {minutes_ago} minutes.")
        return

    for video_data in all_videos:
        video_obj = video_data['video_obj']
        video_published_datetime = video_data['published_dt']

        formatted_message = f"""
    **{video_obj.title}**
    **Creator:** {video_obj.author}
    **Link:** {video_obj.link}
    **Uploaded:** {video_published_datetime.strftime('%Y-%m-%d %H:%M:%S')}
    """
        send_to_discord(DISCORD_WEBHOOK_URL, formatted_message)
        # Add a delay to avoid hitting Discord's rate limits.
        time.sleep(1)


if __name__ == "__main__":
    # The number of minutes to check for new videos.
    MINUTES_TO_CHECK = 5
    main(CHANNEL_IDS, minutes_ago=MINUTES_TO_CHECK)