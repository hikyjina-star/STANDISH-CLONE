from html.parser import HTMLParser
import sys
import os

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.extracted_items = []
        self.forbidden_tags = ['script', 'style', 'head', 'meta', 'link']
        self.tag_stack = []
        self.target_attrs = ['alt', 'title', 'placeholder']

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag.lower())

        # Extract specific attributes
        for attr_name, attr_value in attrs:
            if attr_name.lower() in self.target_attrs and attr_value:
                val = attr_value.strip()
                if val:
                    self.extracted_items.append(f"[ATTR:{attr_name.upper()}] {val}")

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag.lower():
            self.tag_stack.pop()
        elif tag.lower() in self.tag_stack:
            while self.tag_stack and self.tag_stack[-1] != tag.lower():
                self.tag_stack.pop()
            if self.tag_stack:
                self.tag_stack.pop()

    def handle_data(self, data):
        if not data.strip():
            return

        if any(tag in self.forbidden_tags for tag in self.tag_stack):
            return

        text = data.strip()
        if text:
            current_tag = self.tag_stack[-1] if self.tag_stack else "NONE"
            self.extracted_items.append(f"[TAG:{current_tag.upper()}] {text}")

def extract_text_from_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = TextExtractor()
    parser.feed(content)

    seen = set()
    for item in parser.extracted_items:
        if item not in seen:
            print(item)
            seen.add(item)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = "www.standish.ca/en/index.html"
    extract_text_from_file(target_file)
