import os
import re

TARGET_DIR = "www.standish.ca/am/"
VIDEO_URL = "https://youtu.be/ZaNvoO7TTqU?si=KM8xDYpxj4yYUn58"
NEUTRAL_HREF = "javascript:void(0);"

def process_file(filepath, neutralize_only=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Task 2: Neutralize French Translation links
    # Look for anchors with class wpml-ls-link.
    # The previous regex might have been too strict or missed something.
    # Let's try a simpler one:
    content = re.sub(r'href="https://www\.standish\.ca/[^"]+" class="wpml-ls-link"', rf'href="{NEUTRAL_HREF}" class="wpml-ls-link"', content)
    # Also handle the other order if it exists
    content = re.sub(r'class="wpml-ls-link" href="https://www\.standish\.ca/[^"]+"', rf'class="wpml-ls-link" href="{NEUTRAL_HREF}"', content)

    # Social Media links in the footer.
    social_patterns = [
        r'https?://(www\.)?facebook\.com/[^"\'>\s]+',
        r'https?://(www\.)?instagram\.com/[^"\'>\s]+',
        r'https?://(www\.)?linkedin\.com/[^"\'>\s]+',
        r'https?://(www\.)?twitter\.com/[^"\'>\s]+'
    ]

    for pattern in social_patterns:
        # Match only inside <a> tags
        content = re.sub(rf'(<a\s+[^>]*href=)(["\']){pattern}\2', rf'\1\2{NEUTRAL_HREF}\2', content)

    # Task 1: Video Source Replacement (if not index.html)
    if not neutralize_only:
        video_source_patterns = [
            r'https?://(www\.)?youtube\.com/[^"\'>\s]+',
            r'https?://youtu\.be/[^"\'>\s]+',
            r'https?://(www\.)?vimeo\.com/[^"\'>\s]+'
        ]

        for pattern in video_source_patterns:
            # We must be careful not to replace thumbnails/posters.
            # The user said: ONLY modify the source URL/href/src attributes of the actual media player or link.
            # Do NOT alter thumbnail images, poster attributes, background images.

            # Replace in href
            content = re.sub(rf'(href=)(["\']){pattern}\2', rf'\1\2{VIDEO_URL}\2', content)
            # Replace in src
            content = re.sub(rf'(src=)(["\']){pattern}\2', rf'\1\2{VIDEO_URL}\2', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    files = sorted([f for f in os.listdir(TARGET_DIR) if f.endswith(".html")])
    for filename in files:
        path = os.path.join(TARGET_DIR, filename)
        is_index = (filename == "index.html")
        print(f"Processing {path} (Neutralize only: {is_index})")
        process_file(path, neutralize_only=is_index)
