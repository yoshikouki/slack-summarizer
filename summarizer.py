#!/usr/bin/env python3
"""
https://github.com/masuidrive/slack-summarizer
  by [masuidrive](https://twitter.com/masuidrive) @ [Bloom&Co., Inc.](https://www.bloom-and-co.com/)
  2023- [APACHE LICENSE, 2.0](https://www.apache.org/licenses/LICENSE-2.0)
"""
from datetime import datetime, timedelta
import pytz
from slack_sdk.errors import SlackApiError
from lib.constants import CHANNEL_ID, DEBUG, LANGUAGE, SLACK_BOT_TOKEN, TIMEZONE_STR
from lib.openai_api import summarize
from lib.prompt_optimizer import remove_emoji, split_messages_by_token_count
from lib.slack import SlackClient
from lib.utils import retry


def get_time_range():
    """
    Get a time range starting from 25 hours ago and ending at the current time.

    Returns:
        tuple: A tuple containing the start and end times of the time range, as datetime objects.

    Examples:
        >>> start_time, end_time = get_time_range()
        >>> print(start_time, end_time)
        2022-05-17 09:00:00+09:00 2022-05-18 10:00:00+09:00
    """
    hours_back = 25
    timezone = pytz.timezone(TIMEZONE_STR)
    now = datetime.now(timezone)
    yesterday = now - timedelta(hours=hours_back)
    start_time = datetime(yesterday.year, yesterday.month, yesterday.day,
                          yesterday.hour, yesterday.minute, yesterday.second)
    end_time = datetime(now.year, now.month, now.day, now.hour, now.minute,
                        now.second)
    return start_time, end_time


def runner():
    """
    app runner
    """
    slack_client = SlackClient(slack_api_token=SLACK_BOT_TOKEN,
                               summary_channel=CHANNEL_ID)
    start_time, end_time = get_time_range()

    for channel in slack_client.channels:
        channel_id = channel["id"]
        channel_name = channel["name"]
        if DEBUG:
            print(channel_name)
        messages = slack_client.load_messages(channel_id, start_time, end_time)
        if messages is None:
            continue

        # remove emojis in messages
        messages = list(map(remove_emoji, messages))

        result_text = [
            f"{start_time.strftime('%Y-%m-%d')} の #{channel_id} の様子\n"
        ]
        for splitted_messages in split_messages_by_token_count(messages):
            text = summarize("\n".join(splitted_messages), LANGUAGE)
            result_text.append(text)

        summary_text = "\n".join(result_text)
        if DEBUG:
            print(summary_text)
        else:
            retry(lambda: slack_client.post_summary(summary_text, channel_id),
                  exception=SlackApiError)


if __name__ == '__main__':
    runner()
