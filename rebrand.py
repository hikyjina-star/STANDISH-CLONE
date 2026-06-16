import os
import re

# Rule 1: Target Tags
TARGET_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'li', 'label', 'option', 'button']
# Rule 2: Forbidden Tags (Safety)
FORBIDDEN_TAGS = ['script', 'style', 'title', 'meta', 'head', 'link']

# Translation Guide Mappings
MAPPINGS = [
    (r'Standish Communications', 'The Silent Cabal'),
    (r'Standish', 'The Silent Cabal'),
    (r'Agency', 'The Silent Cabal'),
    (r'Marketing', 'Systemic Conditioning'),
    (r'Advertising', 'Subliminal Alignment'),
    (r'Strategy', 'The Grand Design'),
    (r'Branding', 'Identity Imprinting'),
    (r'Web Development', 'Grid Assembly'),
    (r'Digital', 'Etheric Networks'),
    (r'Graphic Design', 'Sigil Crafting'),
    (r'Creative', 'Esoteric Projections'),
    (r'Our Team', 'The Sovereign Council'),
    (r'Experts', 'High Adepts'),
    (r'Portfolio', 'Blueprints'),
    (r'Projects', 'Blueprints'),
    (r'Case Studies', 'Manifestations'),
    (r'CV', 'Ancestral Ledger'),
    (r'Resume', 'Ancestral Ledger'),
    (r'Cover Letter', 'Sovereignty Declaration'),
    (r'Budget', 'Material Tribute'),
    (r'Message', 'Intentions'),
    (r'Submit', 'Seal Destiny'),
    (r'Send', 'Deploy Intention'),
]

def apply_rebrand(text):
    for pattern, replacement in MAPPINGS:
        # 1. UPPERCASE
        text = re.sub(r'\b' + re.escape(pattern.upper()) + r'\b', replacement.upper(), text)
        # 2. Title Case / As is
        text = re.sub(r'\b' + re.escape(pattern) + r'\b', replacement, text)
        # 3. lowercase
        text = re.sub(r'\b' + re.escape(pattern.lower()) + r'\b', replacement.lower(), text)
    return text

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = re.split(r'(<[^>]+>)', content)
    tag_stack = []
    new_parts = []

    for part in parts:
        if part.startswith('<'):
            tag_name_match = re.match(r'<(/?)([a-zA-Z1-6]+)', part)
            if tag_name_match:
                is_closing = tag_name_match.group(1) == '/'
                tag_name = tag_name_match.group(2).lower()
                if is_closing:
                    if tag_stack and tag_stack[-1] == tag_name:
                        tag_stack.pop()
                elif not part.endswith('/>') and tag_name not in ['img', 'br', 'hr', 'input', 'link', 'meta']:
                    tag_stack.append(tag_name)
            new_parts.append(part)
        else:
            is_in_target = any(name in TARGET_TAGS for name in tag_stack)
            is_in_forbidden = any(name in FORBIDDEN_TAGS for name in tag_stack)
            if is_in_target and not is_in_forbidden:
                new_parts.append(apply_rebrand(part))
            else:
                new_parts.append(part)

    result = "".join(new_parts)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

if __name__ == "__main__":
    dir_path = "www.standish.ca/en/"
    html_files = [
        "agency.html", "careers.html", "contact.html", "form-careers.html",
        "form-contact.html", "form-project.html", "form-support.html",
        "index.html", "projects.html", "services.html"
    ]
    for filename in html_files:
        filepath = os.path.join(dir_path, filename)
        if os.path.exists(filepath):
            process_file(filepath)
