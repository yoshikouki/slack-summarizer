import re

import emoji

from lib.constants import MAX_BODY_TOKENS


def remove_emoji(text: str) -> str:
    """
    Remove emojis from the given text.

    Args:
        text (str): A string containing the text to remove custom emojis from.

    Returns:
        str: The input text with custom emojis removed.

    Example:
        >>> text = "Hello, world! :smile: :wave:"
        >>> remove_custom_emoji(text)
        'Hello, world!  '
    """
    # Remove Unicode emojis
    text = emoji.replace_emoji(text, replace='')

    # Remove Slack custom emojis
    custom_pattern = r":[-_a-zA-Z0-9]+?:"
    text = re.sub(custom_pattern, "", text)
    return text


def estimate_openai_chat_token_count(text: str) -> int:
    """
    Estimate the number of OpenAI API tokens that would be consumed by sending the given text to the chat API.

    Args:
        text (str): The text to be sent to the OpenAI chat API.

    Returns:
        int: The estimated number of tokens that would be consumed by sending the given text to the OpenAI chat API.

    Examples:
        >>> estimate_openai_chat_token_count("Hello, how are you?")
        7
    """
    # Split the text into words and count the number of characters of each type
    pattern = re.compile(
        r"""(
            \d+       | # digits
            [a-z]+    | # alphabets
            \s+       | # whitespace
            .           # other characters
            )""", re.VERBOSE | re.IGNORECASE)
    matches = re.findall(pattern, text)

    # based on https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
    def counter(tok):
        if tok == ' ' or tok == '\n':
            return 0
        elif tok.isdigit() or tok.isalpha():
            return (len(tok) + 3) // 4
        else:
            return 1

    return sum(map(counter, matches))


def split_messages_by_token_count(messages: list[str]) -> list[list[str]]:
    """
    Split a list of strings into sublists with a maximum token count.

    Args:
        messages (list[str]): A list of strings to be split.

    Returns:
        list[list[str]]: A list of sublists, where each sublist has a token count less than or equal to max_body_tokens.
    """
    body_token_counts = [
        estimate_openai_chat_token_count(message) for message in messages
    ]
    result = []
    current_sublist = []
    current_count = 0

    for message, count in zip(messages, body_token_counts):
        if current_count + count <= MAX_BODY_TOKENS:
            current_sublist.append(message)
            current_count += count
        else:
            result.append(current_sublist)
            current_sublist = [message]
            current_count = count

    result.append(current_sublist)
    return result
