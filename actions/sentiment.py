# Adapted from https://cloud.google.com/natural-language/docs/analyzing-sentiment#language-sentiment-file-python
import enum

from google.cloud import language_v1


class Sentiment(enum.Enum):
    clearly_positive = 0
    clearly_negative = 1
    neutral = 2
    mixed = 3


def sample_analyze_sentiment(text_content: str) -> Sentiment:
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})

    return parse_sentiment(response.document_sentiment.score, response.document_sentiment.magnitude)


def parse_sentiment(score: float, magnitude: float) -> Sentiment:
    if abs(score) > 0.25:
        return Sentiment.clearly_positive if score > 0 else Sentiment.clearly_negative
    else:
        return Sentiment.mixed if magnitude > 0.3 else Sentiment.neutral
