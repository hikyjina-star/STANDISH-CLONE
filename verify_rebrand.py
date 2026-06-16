import os
import re

TARGET_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'li', 'label', 'option', 'button']
BANNED_TERMS = ['Standish', 'Agency', 'Marketing', 'Advertising', 'Strategy', 'Branding', 'Web Development', 'Digital', 'Graphic Design', 'Creative']

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = re.split(r'(<[^>]+>)', content)
    tag_stack = []
    failures = []

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
        else:
            is_in_target = any(name in TARGET_TAGS for name in tag_stack)
            if is_in_target:
                for term in BANNED_TERMS:
                    if term.lower() in part.lower():
                        failures.append(f"Found '{term}' in <{tag_stack[-1]}>: {part.strip()}")

    return failures

if __name__ == "__main__":
    dir_path = "www.standish.ca/en/"
    html_files = [
        "agency.html", "careers.html", "contact.html", "form-careers.html",
        "form-contact.html", "form-project.html", "form-support.html",
        "index.html", "projects.html", "services.html"
    ]
    all_pass = True
    for filename in html_files:
        filepath = os.path.join(dir_path, filename)
        if os.path.exists(filepath):
            fails = audit_file(filepath)
            if fails:
                print(f"FAIL: {filename}")
                for f in fails:
                    print(f"  {f}")
                all_pass = False
            else:
                print(f"PASS: {filename}")

    if all_pass:
        print("\nALL FILES ARE CLEAN.")
