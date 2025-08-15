import requests
from bs4 import BeautifulSoup

def extract_job_post_content(url):
    """
    Fetches the job post content from a URL and extracts main text for use in email generation.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Try to extract main content heuristically
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40])
        if not text:
            # fallback: get all text
            text = soup.get_text(separator=' ', strip=True)
        # Limit to first 800 chars for brevity
        return text[:800] + ('...' if len(text) > 800 else '')
    except Exception as e:
        return f"[Could not extract job post: {e}]"
def generate_email(recipient, company, product, pain_point, tone, custom_message):
    """
    Generate a cold email based on the provided parameters.
    """
    greetings = {
        "Professional": f"Dear {recipient},",
        "Friendly": f"Hi {recipient},",
        "Persuasive": f"Hello {recipient},",
        "Casual": f"Hey {recipient},",
    }
    intro = f"I hope this message finds you well. My name is [Your Name], and I wanted to reach out regarding {company}'s challenges with {pain_point}."
    body = f"At [Your Company], we offer {product} that can help you overcome {pain_point} and boost your team's productivity."
    closing = "If you're interested, I'd love to schedule a quick call to discuss how we can help. Looking forward to your response!"
    if custom_message.strip():
        body += f"\n\n{custom_message.strip()}"
    email = (
        f"{greetings.get(tone, 'Hello')}\n\n"
        f"{intro}\n\n"
        f"{body}\n\n"
        f"{closing}\n\n"
        f"Best regards,\n[Your Name]"
    )
    return email
import re

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.strip()
    text = ' '.join(text.split())
    return text
