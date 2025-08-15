import re

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        '',
        text
    )  # Remove URLs
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Keep only alphanumeric + spaces
    text = re.sub(r'\s{2,}', ' ', text)  # Collapse spaces
    return text.strip()
