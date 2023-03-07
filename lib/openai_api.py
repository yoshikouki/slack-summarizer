import openai

from lib.constants import CHAT_MODEL, OPEN_AI_TOKEN, TEMPERATURE, DEBUG

# Set OpenAI API key
openai.api_key = OPEN_AI_TOKEN


def summarize(text: str, language: str = "Japanese"):
    """
    Summarize a chat log in bullet points, in the specified language.

    Args:
        text (str): The chat log to summarize, in the format "Speaker: Message" separated by line breaks.
        language (str, optional): The language to use for the summary. Defaults to "Japanese".

    Returns:
        str: The summarized chat log in bullet point format.

    Examples:
        >>> summarize("Alice: Hi\nBob: Hello\nAlice: How are you?\nBob: I'm doing well, thanks.")
        '- Alice greeted Bob.\n- Bob responded with a greeting.\n- Alice asked how Bob was doing.\n- Bob replied that he was doing well.'
    """
    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        temperature=TEMPERATURE,
        messages=[{
            "role":
            "system",
            "content":
            "\n".join([
                "You are a great summarizer of the chat log overview by subject.",
                "The summary should focus on the theme of the conversation rather than the person's movements.",
                'The chat logs format consists of one line per message in the format "Speaker: Message".',
                "The `\\n` within the message represents a line break."
                f'The user understands {language} only.',
                f'So, The assistant need to speak in {language}.',
            ])
        }, {
            "role":
            "user",
            "content":
            "\n".join([
                f"Please meaning summarize the following chat logs to flat bullet list in {language}.",
                "The summary should focus on the theme of the conversation rather than the person's movements.",
                "It isn't line by line summary.",
                "Do not include greeting/salutation/polite expressions in summary.",
                "With make it easier to read."
                f"Write in {language}.",
                "chat logs:",
                text,
            ])
        }])

    if DEBUG:
        print(response["choices"][0]["message"]['content'])
    return response["choices"][0]["message"]['content']
