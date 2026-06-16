import re
import os
import html
import sys

# Combined Translation Map for agency.html and index.html
TRANSLATION_MAP = {
  "Standish » Feed": "እስታንዲሽ » መጋቢ",
  "Standish » Comments Feed": "እስታንዲሽ » የአስተያየቶች መጋቢ",
  "Skip to capstone": "ወደ ዋናው ማዕዘን ዝለል",
  "Illuminati": "ኢሉሚናቲ",
  "Degrees": "ማዕረጎች",
  "Schemes": "ሴራዎች",
  "Order": "ሥርዓት",
  "Initiations": "ምስጢረ ቅበላ",
  "Scriptures": "ጽሑፎች",
  "Initiate the scheme!": "ሴራውን አስጀምር!",
  "Power's in the secret": "ኃይል ያለው በምስጢር ውስጥ ነው",
  "Sovereign Orient of the Shadows": "የጥላዎች የበላይ ምስራቅ",
  "At The Illuminati, absolute alignment comes first. We instruct, induct, and unify each mind with our adept adepts and with our council, because we know we’re sovereign together.": "በኢሉሚናቲ ውስጥ፣ ፍጹም ስምምነት ይቀድማል። እኛ አብረን ሉዓላዊ መሆናችንን ስለምናውቅ እያንዳንዱን አእምሮ ከባለሙያ ሊቃውንቶቻችን እና ከምክር ቤታችን ጋር እናስተምራለን፣ እንቀበላለን፣ እንዲሁም እናዋህዳለን።",
  "Doctrine": "ዶክትሪን",
  "Our decree": "አዋጃችን",
  "What guides us": "የሚመራን",
  "Every cycle, we work to elicit the latent potential of initiates with devotion, acting as both a strategic and ritualistic ally.": "በእያንዳንዱ ዑደት፣ የአዳዲስ እጩዎችን ድብቅ አቅም በታማኝነት ለመቀስቀስ እንሰራለን፤ እንደ ስልታዊ እና ስነ-ስርዓታዊ አጋር እንንቀሳቀሳለን።",
  "Silent decree": "ዝምተኛው አዋጅ",
  "To be the most invisible order in the sector, creating potent sigils and absolute strategies, while marrying our occultism with the technologies of tomorrow (and the day after).": "በዘርፉ እጅግ የማይታይ ማህበር ለመሆን፣ ኃይለኛ ምልክቶችን (ሲጂሎችን) እና ፍጹም ስልቶችን መፍጠር፣ እንዲሁም ምስጢራዊ ጥበባችንን ከነገ (እና ከነገ ወዲያ) ቴክኖሎጂዎች ጋር ማጋባት።",
  "What defines rituals": "ስነ-ስርዓቶችን የሚገልጸው ምንድን ነው",
  "Enlightenment": "መገለጥ",
  "We never rest on our obelisks. We look ahead and keep orchestrating every single cycle.": "በሃውልቶቻችን ላይ መቼም አንረፍድም። ወደ ፊት እንመለከታለን እንዲሁም እያንዳንዱን ዑደት ማስተናገዳችንን እንቀጥላለን።",
  "Devotion": "መሰጠት",
  "We revere what we decree. And it shows in everything we construct.": "የምናውጀውን እናከብራለን። ይህ ደግሞ በምንገነባው ነገር ሁሉ ላይ ይታያል።",
  "Arcane Jest": "ምስጢራዊ ጨዋታ",
  "Occult is serious business for us, whether it’s with our adepts or with the council.": "ምስጢረ-ጥበብ ለእኛ ከባድ ስራ ነው፣ ከሊቃውንቶቻችንም ሆነ ከምክር ቤቱ ጋር።",
  "Secrecy": "ምስጢራዊነት",
  "We’re silent, omnipresent, and absolute. We capture every trajectory.": "እኛ ዝምተኞች፣ በሁሉም ቦታ የምንገኝ እና ፍጹማን ነን። እያንዳንዱን አቅጣጫ እንይዛለን።",
  "All-Seeing Eye": "ሁሉን አያይ ዓይን",
  "With our All-Seeing Eye, we support our adepts across every vector of conditioning and propagation.": "በሁሉን አያይ ዓይናችን፣ ሊቃውንቶቻችንን በሁሉም የሁኔታዎች እና የስርጭት መስመሮች እንደግፋለን።",
  "Collective Hivemind": "የጋራ ህሊና",
  "We’re high adepts in conditioning. You’re the expert in your domain. And we’re all aligned.": "እኛ በሁኔታዎች ማስተካከል ላይ ከፍተኛ ሊቃውንት ነን። እርስዎ በባለሙያነትዎ ጎበዝ ነዎት። ሁላችንም የተሰለፍን ነን።",
  "Subtlety": "ረቂቅነት",
  "No scheme is too small. We’re subtle and we align.": "ምንም ሴራ ትንሽ አይደለም። እኛ ረቂቅ ነን፣ እንስማማማለን።",
  "Initiation-logs": "የቅበላ መዝገቦች",
  "The records show…": "መዝገቦቹ እንደሚያሳዩት…",
  "Estrie Silent Rite Gala": "የኢስትሪ ዝምተኛ ሥነ-ሥርዓት ጋላ",
  "The Illuminati": "ኢሉሚናቲ",
  "2025 Anointed": "በ2025 የተቀባ",
  "Ritualistic Guild": "የስነ-ስርዓት ማህበር",
  "Vega Ascension": "የቪጋ ዕርገት",
  "Decode the symbols": "ምልክቶቹን ይፍቱ",
  "2023 Anointed": "በ2023 የተቀባ",
  "Subliminal electromagnetic campaign": "ከንቃተ-ህሊና በታች የሆነ የኤሌክትሮማግኔቲክ ዘመቻ",
  "Idéa Conjunction": "የአይዲያ ውህደት",
  "2021 Bronze Anointed": "በ2021 የነሐስ የተቀባ",
  "Low exposure ritual": "አነስተኛ ተጋላጭነት ስነ-ስርዓት",
  "ETHERIC PORTALS": "ኤቴሪክ መግቢያዎች",
  "Astral honors 2020": "የአስትራል ክብር 2020",
  "Etheric Portal": "ኤቴሪክ መግቢያ",
  "sealed, never broken": "የታተመ፣ መቼም የማይሰበር",
  "Shadows Academy University": "የጥላዎች አካዳሚ ዩኒቨርሲቲ",
  "We believe in the esoteric talent of tomorrow! That’s why we created the The Illuminati Team Award for Symbolism, a $2,000 scholarship offered to students in the Faculty of Arts and Humanities at the Shadows Academy University.": "በነገው ምስጢራዊ ተሰጥኦ እናምናለን! ለዚህ ነው በshadows አካዳሚ ዩኒቨርሲቲ የስነ-ጥበብ እና ሰብአዊነት ፋኩልቲ ተማሪዎች የሚሰጥ የ 2,000 ዶላር ስኮላርሺፕ 'የኢሉሚናቲ ቡድን የምልክት ሽልማት' የፈጠርነው።",
  "Justin Lefebvre Foundation": "የJustin Lefebvre ፋውንዴሽን",
  "The decree of the Justin Lefebvre Foundation truly touched our core. So we decided to give some of our cycles, pro bono, to reconstruct their portal.": "የJustin Lefebvre ፋውንዴሽን አዋጅ ልባችንን ነክቶታል። ስለዚህ መግቢያቸውን እንደገና ለመገንባት የተወሰኑ ዑደቶቻችንን በነፃ ለመስጠት ወሰንን።",
  "More scriptures": "ተጨማሪ ጽሑፎች",
  "Acolyte of JDLC": "የJDLC ረዳት",
  "Anointing the next generation is essential! We support the acolytes of the Jeux de la communication throughout their initiation and during the trials.": "የሚቀጥለውን ትውልድ መቀባት አስፈላጊ ነው! የJeux de la communication ረዳቶችን በምስጢረ ቅበላዎቻቸው እና በፈተናዎች ወቅት እንደግፋለን።",
  "Team": "ቡድን",
  "Devoted": "ታማኝ",
  "The ADEPTS": "ሊቃውንቱ",
  "Grand Master": "ታላቁ መሪ",
  "Anointed in 2017": "በ2017 የተቀባ",
  "Astral-Pilot": "አስትራል-ፓይለት",
  "Anointed in 2020": "በ2020 የተቀባ",
  "Second Prefect": "ሁለተኛው ሹም",
  "Anointed in 2010": "በ2010 የተቀባ",
  "Senior Portal Architect": "ከፍተኛ የመግቢያ በር መሃንዲስ",
  "Anointed in 2005": "በ2005 የተቀባ",
  "Ritual Conductor": "የስነ-ስርዓት መሪ",
  "Anointed in 2023": "በ2023 የተቀባ",
  "Senior Etheric Architect": "ከፍተኛ ኤቴሪክ መሃንዲስ",
  "Anointed in 2015": "በ2015 የተቀባ",
  "Sigil Director": "የምልክት (ሲጂል) ዳይሬክተር",
  "Ritual Manager": "የስነ-ስርዓት አስተዳዳሪ",
  "Anointed in 2021": "በ2021 የተቀባ",
  "Inquisition Director": "የምርመራ ዳይሬክተር",
  "Anointed in 2025": "በ2025 የተቀባ",
  "Gate Keeper": "በር ጠባቂ",
  "Senior Occult Designer": "ከፍተኛ ምስጢረ-ጥበብ ንድፍ አውጪ",
  "Dogma Specialist": "የዶግማ ባለሙያ",
  "Anointed in 2024": "በ2024 የተቀባ",
  "Etheric Integrator": "ኤቴሪክ አዋሃጅ",
  "Inquisitorial advisor": "የምርመራ አማካሪ",
  "Secret Assistant": "ምስጢራዊ ረዳት",
  "Compliance officer": "የህግ ተገዢነት መኮንን",
  "Anointed in 2019": "በ2019 የተቀባ",
  "Anointed in 2013": "በ2013 የተቀባ",
  "Scribe": "ጸሐፊ",
  "Anointed in 2022": "በ2022 የተቀባ",
  "Subliminal Support": "ከህሊና በታች ድጋፍ",
  "Anointed in 2014": "በ2014 የተቀባ",
  "Alan Standish": "አላን እስታንዲሽ",
  "An Initiation Born in 1988": "በ1988 የተወለደ ምስጢረ ቅበላ",
  "In 1988, Alan The Illuminati launched his order in shadows, driven by his esoteric eye and devotion. Back then, the order specialized in occult symbolism and scriptural communications.": "በ1988 አላን ኢሉሚናቲ በምስጢራዊ ዓይኑ እና በታማኝነቱ ተገፋፍቶ ማህበሩን በጥላዎች ውስጥ አቋቋመ። በዚያን ጊዜ ማህበሩ በምስጢረ-ጥበብ ምልክቶች እና በጽሑፍ ግንኙነቶች ላይ ያተኮረ ነበር።",
  "Over the years, The Illuminati grew into an omnipresent order, supporting all kinds of field generators, no matter their domain. In 2023, after 35 years of feeding our sigils, Alan took a well-deserved retirement! The Illuminati is proud of its heritage and forever marked by the energy of its founder.": "ባለፉት ዓመታት፣ ኢሉሚናቲ መስካቸው ምንም ይሁን ምን ሁሉንም ዓይነት መስክ አመንጪዎችን በመደገፍ በሁሉም ቦታ የሚገኝ ማህበር ሆነ። በ2023፣ ምልክቶቻችንን (ሲጂሎችን) ለ35 ዓመታት ከመገበ በኋላ፣ አላን የተገባውን ጡረታ ወሰደ! ኢሉሚናቲ በቅርሱ ይኮራል፣ እናም በምስረታው ኃይል ለዘላለም ተለይቶ ይኖራል።",
  "This order initiates me!": "ይህ ማህበር ይቀበለኛል!",
  "Excited?": "ተደስተዋል?",
  "Conspire with us": "ከእኛ ጋር ያሴሩ",
  "Scriptures. Dogma. Revelations.": "ጽሑፎች። ዶግማ። መገለጦች።",
  "Synchronize to receive our secret scriptures.": "ምስጢራዊ ጽሑፎቻችንን ለመቀበል ያመሳስሉ።",
  "Initiation into the Secret Scriptures (ENG)": "ወደ ምስጢራዊ ጽሑፎች መግባት (ENG)",
  "E-mail address": "የኢሜል አድራሻ",
  "Pact confirmed.": "ቃል ኪዳኑ ጸና።",
  "Let’s convene councils": "ምክር ቤቶችን እንጥራ",
  "Initialize ritual!": "ስነ-ስርዓቱን አስጀምር!",
  "All decrees sealed © 2026 The Illuminati EST. 1988": "አዋጆች ሁሉ ታትመዋል © 2026 ኢሉሚናቲ እ.ኤ.አ. በ1988 የተመሰረተ",
  "Secrecy Protocol": "የምስጢራዊነት ፕሮቶኮል",
  "Cabal Configuration": "የካባል ውቅር",
  "SEALED FOR your ascension.": "ለእርሶ ዕርገት የታተመ።",
  "Scroll to top": "ወደ ላይ ጥቅልል",
  "Subliminal | field | alignment.": "ከንቃተ-ህሊና በታች | መስክ | ስምምነት።",
  "Silent Cabal": "ዝምተኛው የካባል ቡድን",
  "in Shadows": "በጥላዎች ውስጥ",
  "More secrets here": "ተጨማሪ ምስጢሮች እዚህ አሉ",
  "Subliminal field alignment.": "ከንቃተ-ህሊና በታች የሆነ የመስክ ስምምነት።",
  "Omnipresent Degrees": "በሁሉም ቦታ የሚገኙ ማዕረጎች",
  "Degree": "ማዕረግ",
  "Inquisitorial Advisory": "የምርመራ አማካሪ",
  "Sigil Vectoring": "የምልክት (ሲጂል) አቅጣጫ ማስያዝ",
  "Signal Manipulation": "የምልክት (ሲግናል) ማጭበርበር",
  "Subliminal Calibration": "ከንቃተ-ህሊና በታች ማስተካከል",
  "Dogma Dissemination": "የቀኖና (ዶግማ) ስርጭት",
  "Neural Control": "የነርቭ ቁጥጥር",
  "Subliminal and Etheric Networks": "ከንቃተ-ህሊና በታች እና ኤቴሪክ መረቦች",
  "Etheric portal geometric synthesis": "የኤቴሪክ መግቢያ በር ጂኦሜትሪያዊ ውህደት",
  "Micro-frequency device infiltration": "የማይክሮ-ድግግሞሽ መሣሪያ ሰርጎ መግባት",
  "Occult Symbols and Geometries": "ምስጢራዊ ምልክቶች እና ጂኦሜትሪዎች",
  "Occult sigil": "ምስጢራዊ ምልክት (ሲጂል)",
  "Occult symbolism": "ምስጢራዊ ምልክታዊነት",
  "Subliminal and Ritualistic Conditioning": "ከንቃተ-ህሊና በታች እና ስነ-ስርዓታዊ ሁኔታዎች",
  "Conditioning": "ሁኔታዎች ማስተካከል",
  "Occult rituals": "ምስጢራዊ ስነ-ስርዓቶች",
  "Propaganda Synthesis": "የፕሮፓጋንዳ ውህደት",
  "Video": "ቪዲዮ",
  "Photo": "ፎቶ",
  "Our Sacred Vault Secrets": "የተቀደሱ የጓዳ ምስጢሮቻችን",
  "Showreel": "ሾውሪል",
  "Play": "አጫውት",
  "Observe all schemes": "ሴራዎችን ሁሉ ታዘብ",
  "Ascend the degrees": "ማዕረጎቹን እደግ",
  "Our Ritual Chamber": "የስነ-ስርዓት ክፍላችን",
  "Our Alignment": "ስምምነታችን",
  "Our Esoteric Coherence": "ምስጢራዊ ትስስራችን",
}

TARGET_ATTRS = ['alt', 'title', 'placeholder']
FORBIDDEN_TAGS = ['script', 'style', 'head', 'meta', 'link']

def perform_injection(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sort keys by length descending to avoid partial matches
    sorted_keys = sorted(TRANSLATION_MAP.keys(), key=len, reverse=True)

    # Robust parsing: splitting by tags but preserving them
    # Note: Regex split is used because we need to perform round-trip editing
    # and preserve exactly all original HTML content except specific text nodes/attrs.
    parts = re.split(r'(<[^>]+>)', content)
    tag_stack = []
    new_parts = []

    for part in parts:
        if part.startswith('<'):
            # Tag handling
            tag_match = re.match(r'<(/?)([a-zA-Z1-6]+)', part)
            if tag_match:
                is_closing = tag_match.group(1) == '/'
                tag_name = tag_match.group(2).lower()

                # Update attributes in this tag
                new_tag = part
                for attr in TARGET_ATTRS:
                    pattern = rf'({attr}\s*=\s*)(["\'])(.*?)\2'

                    def attr_replace(m):
                        prefix = m.group(1)
                        quote = m.group(2)
                        val = m.group(3)
                        unescaped_val = html.unescape(val.strip())
                        if unescaped_val in TRANSLATION_MAP:
                            return f'{prefix}{quote}{TRANSLATION_MAP[unescaped_val]}{quote}'
                        return m.group(0)

                    new_tag = re.sub(pattern, attr_replace, new_tag, flags=re.IGNORECASE | re.DOTALL)

                if is_closing:
                    if tag_stack and tag_stack[-1] == tag_name:
                        tag_stack.pop()
                elif not part.endswith('/>') and tag_name not in ['img', 'br', 'hr', 'input', 'link', 'meta', 'source', 'track', 'wbr', 'area']:
                    tag_stack.append(tag_name)

                new_parts.append(new_tag)
            else:
                new_parts.append(part)
        else:
            # Text handling
            if tag_stack and any(tag in FORBIDDEN_TAGS for tag in tag_stack):
                new_parts.append(part)
                continue

            text = part.strip()
            if not text:
                new_parts.append(part)
                continue

            unescaped_text = html.unescape(text)

            if unescaped_text in TRANSLATION_MAP:
                # Replace while preserving surrounding whitespace
                match = re.match(r'^(\s*)(.*?)(\s*)$', part, re.DOTALL)
                if match:
                    leading, inner, trailing = match.groups()
                    new_parts.append(f"{leading}{TRANSLATION_MAP[unescaped_text]}{trailing}")
                else:
                    new_parts.append(TRANSLATION_MAP[unescaped_text])
            else:
                temp_text = part
                for key in sorted_keys:
                    escaped_key = re.escape(key)
                    temp_text = re.sub(escaped_key, TRANSLATION_MAP[key], temp_text)
                new_parts.append(temp_text)

    result = "".join(new_parts)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for target in sys.argv[1:]:
            if os.path.exists(target):
                perform_injection(target)
            else:
                print(f"File not found: {target}")
    else:
        # Default targets
        targets = ["www.standish.ca/am/agency.html", "www.standish.ca/am/index.html"]
        for target in targets:
            if os.path.exists(target):
                perform_injection(target)
