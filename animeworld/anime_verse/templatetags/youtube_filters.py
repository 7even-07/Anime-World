import re
from django import template

register = template.Library()

@register.filter
def youtube_embed(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)

    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}?rel=0"

    return url