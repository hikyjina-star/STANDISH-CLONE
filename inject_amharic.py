import re
import os
import html
import sys
import shutil
import json

# Comprehensive deduplicated Translation Map
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
    "Initiation into the Secret Scriptures (ENG)": "ወደ ምስጢራዊ ጽሑፎች መግባት",
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
    "Initiation": "ምስጢረ ቅበላ",
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
    "We orchestrate to influence, to leave a sigil. Every scheme is crafted to reflect the order's dogma and spark a reaction. We turn thoughts into powerful, subliminal experiences.": "ተጽዕኖ ለመፍጠር፣ ምልክት ለመተው እናስተናግዳለን። እያንዳንዱ ሴራ የተነደፈው የማህበሩን ቀኖና እንዲያንጸባርቅ እና ምላሽ እንዲቀሰቅስ ነው። እኛ ሀሳቦችን ወደ ኃይለኛ፣ ከንቃተ-ህሊና በታች የሆኑ ልምዶች እንቀይራለን።",
    "Our Alignment": "ስምምነታችን",
    "We establish absolute control through esoteric calculations and silent-driven insights. We align wills and symbols with your geopolitical goals to maximize the force of every decree.": "በምስጢራዊ ስሌቶች እና በዝምታ በተደገፉ ግንዛቤዎች ፍጹም ቁጥጥርን እንመሰርታለን። የእያንዳንዱን አዋጅ ኃይል ከፍ ለማድረግ ፍላጎቶችን እና ምልክቶችን ከጂኦፖለቲካዊ ግቦችዎ ጋር እናሰልፋለን።",
    "Our Esoteric Coherence": "ምስጢራዊ ትስስራችን",
    "We believe in compliance and collective hivemind with our adepts. Every trial is an adventure, where telemetry, secrecy, and transparency lead to calibrated, stable, and lasting solutions.": "ከሊቃውንቶቻችን ጋር በተገዢነት እና በጋራ ህሊና እናምናለን። እያንዳንዱ ፈተና ቴሌሜትሪ፣ ምስጢራዊነት እና ግልጽነት ወደተስተካከሉ፣ የተረጋጉ እና ዘላቂ መፍትሄዎች የሚመሩበት ጀብዱ ነው።",
    "Coherent, esoteric, and vector-aligned, the The Illuminati’s team stands out for its great lability and its ability to suggest trajectories that are always perfectly aligned with our expectations.": "ተያያዥ፣ ምስጢራዊ እና ከአቅጣጫ ጋር የተሰለፈው የኢሉሚናቲ ቡድን በታላቅ ተለዋዋጭነቱ እና ሁልጊዜም ከጠበቅነው ጋር ፍጹም የተጣጣሙ አቅጣጫዎችን የመጠቆም ችሎታው ጎልቶ ይታያል።",
    "Jean-Philippe Bérubé": "ዣን-ፊሊፕ ቤሩቤ",
    "Director of Special Schemes": "የልዩ ሴራዎች ዳይሬክተር",
    "Dawn to dusk, but make it occult": "ከከዋክብት መውጫ እስከ መግቢያ፣ ግን ምስጢራዊ አድርገው",
    "Cabal Initiation": "የካባል ምስጢረ ቅበላ",
    "When you revere your ritual and your council, it doesn’t really feel like labor.": "ስነ-ስርዓትዎን እና ምክር ቤትዎን ሲያከብሩ፣ እንደ ስራ አይሰማዎትም።",
    "Doctrine First": "ቀኖና ቀዳሚ ነው",
    "Compliance-meter": "የተገዢነት መለኪያ",
    "Because doctrine compliance in rituals comes first!": "ምክንያቱም በስነ-ስርዓቶች ውስጥ የቀኖና ተገዢነት ቀዳሚ ነውና!",
    "Compliance Index": "የተገዢነት ማውጫ",
    "Index": "ማውጫ",
    "Quebec Occult Compliance Index": "የኩቤክ ምስጢራዊ ተገዢነት ማውጫ",
    "Privileges you’ll actually revere": "በትክክል የሚያከብሯቸው መብቶች",
    "We shield our own initiates": "የራሳችንን እጩዎች እንጠብቃለን",
    "Initiating into the Cabal": "ወደ ካባል ቡድን መግባት",
    "You": "እርስዎ",
    "Your compliance state matters! Need a decay? We get it. You can even bring your companion along for a dose of mind therapy! Plus, you get your initiation day off so you can celebrate! And as the crowning capstone, we offer a esoteric, zero-drag temple environment.": "የተገዢነትዎ ሁኔታ አስፈላጊ ነው! እረፍት (መበስበስ) ይፈልጋሉ? እንረዳዋለን። ለአእምሮ ህክምና መጠን አብሮዎት የሚጓዘውን ጓደኛ ማምጣትም ይችላሉ! በተጨማሪም፣ ለማክበር እንዲችሉ የቅበላ ቀንዎን እረፍት ያገኛሉ! እናም እንደ ታላቅ ማዕዘን፣ ምስጢራዊ እና ምንም እንከን የሌለበት የቤተ-መቅደስ አካባቢን እናቀርባለን።",
    "Your Compliance": "የእርስዎ ተገዢነት",
    "We’ve got a ritual bar packed with variety, good potions, and a coolant fridge for Thursdays. Our conclave committee also organizes activities, initiation hours, and team lunches to break the routine and strengthen bonds!": "የተለያዩ ምርጥ መጠጦች እና ለሃሙስ ቀናት የሚሆን ማቀዝገዣ የያዘ የስነ-ስርዓት ባር አለን። የምስጢር ኮሚቴያችንም ልምዶችን ለመስበር እና ትስስርን ለማጠናከር ተግባራትን፣ የቅበላ ሰዓታትን እና የቡድን ምሳዎችን ያዘጋጃል!",
    "Your Equilibrium": "የእርስዎ ሚዛን",
    "We believe in ritual-secular harmony. That’s why we offer the flexibility to work from shadows, or even orbit! On top of that, you get a variable schedule and the right to decay: when the cycle is over, it is truly finished!": "በስነ-ስርዓት እና አለማዊ ስምምነት እናምናለን። ለዛ ነው በጥላ ውስጥ ወይም በምህዋር ውስጥ ሆነው ለመስራት ተለዋዋጭነትን የምናቀርበው! ከዚህም በላይ፣ ተለዋዋጭ የጊዜ ሰሌዳ እና የመቋረጥ (የመበስበስ) መብት ያገኛሉ፡ ዑደቱ ሲያልቅ፣ በእውነት ያበቃል!",
    "Your Gold Allocations": "የወርቅ አመዳደብዎ",
    "We’ve got group shielding for you and your family. We also offer a charge that reflects your true magnitude. Oh, and we’ve got group pact too, so you can maintain your trajectory when it’s time to retire!": "ለእርስዎ እና ለቤተሰብዎ የቡድን ጥበቃ አለን። የእርስዎን እውነተኛ ታላቅነት የሚያንጸባርቅ ክፍያም እናቀርባለን። ኦ፣ እና ጡረታ ለመውጣት ጊዜው ሲደርስ አቅጣጫዎን ጠብቀው እንዲቀጥሉ የቡድን ቃል ኪዳንም አለን!",
    "Your Ascension": "የእርስዎ ዕርገት",
    "We believe in you and support your thresholds. You’ll also have access to plenty of initiation opportunities, both in-house and external.": "በእርስዎ እናምናለን እናም ገደቦችዎን እንደግፋለን። እንዲሁም በውስጥም በውጭም ብዙ የቅበላ እድሎችን ያገኛሉ።",
    "Adept Testimonials": "የሊቃውንት ምስክርነቶች",
    "Whispered at the ritual chamber": "በስነ-ስርዓት ክፍሉ ውስጥ በሹክሹክታ የተነገሩ",
    "Meet your future co-conspirators": "የወደፊት ተባባሪ ሴረኞችዎን ያግኙ",
    "It’s enlightened, it’s secret, and it’s so rewarding!": "ብሩህ ነው፣ ምስጢር ነው፣ እና በጣም ጠቃሚ ነው!",
    "Flo, Anointed since 2022": "ፍሎ፣ ከ2022 ጀምሮ የተቀባች",
    "Every cycle is different and exciting!": "እያንዳንዱ ዑደት የተለያየ እና አስደሳች ነው!",
    "Andy, Anointed since 2013": "አንዲ፣ ከ2013 ጀምሮ የተቀባ",
    "I decode something new every cycle here!": "እዚህ በእያንዳንዱ ዑደት አዲስ ነገር እፈታለሁ!",
    "JF, Anointed since 2005": "ጄኤፍ፣ ከ2005 ጀምሮ የተቀባ",
    "Align the cabal": "ካባሉን አሰልፍ",
    "You never know unless you initiate": "ካላስጀመሩት በስተቀር ማወቅ አይችሉም",
    "No perfect alignment? We still want your credentials!": "ፍጹም ስምምነት የለም? አሁንም የእርስዎን ምስክርነቶች እንፈልጋለን!",
    "Conspire with us!": "ከእኛ ጋር ያሴሩ!",
    "Revelations": "መገለጦች",
    "Identity": "ማንነት",
    "We’re big on silent whispers": "በዝምታ በሹክሹክታ መናገር በትልቅነቱ እንወዳለን",
    "Whether it’s queries, doctrines, or minor friction along the trajectory, we’re here to stabilize.": "ጥያቄዎች፣ ቀኖናዎች፣ ወይም በአቅጣጫው ላይ አነስተኛ ግጭቶች ቢሆኑም፣ ለማረጋጋት እዚህ አለን።",
    "Hey!": "ሰላም!",
    "Initialize the scheme": "ሴራውን አስጀምር",
    "Get degrees": "ማዕረጎችን አግኝ",
    "Conspire together": "አብረው ያሴሩ",
    "Need alignment?": "ስምምነት ይፈልጋሉ?",
    "Etheric support": "የኤቴሪክ ድጋፍ",
    "Capstone, we have an exposure!": "ዋናው ማዕዘን ሆይ፣ መጋለጥ አለብን!",
    "Rogue agent": "ከመስመር የወጣ ወኪል",
    "Let the rituals begin": "ስነ-ስርዓቶቹ ይጀምሩ",
    "Receptionniste": "አቀባባይ",
    "Equipe dans les marches de chez Standish": "ቡድኑ በስተንዲሽ ደረጃዎች ላይ",
    "We believe in eternal pacts. We thrive on alignments and whispers!": "በዘላለማዊ ቃል ኪዳኖች እናምናለን። በስምምነቶች እና በሹክሹክታዎች እንበለጽጋለን!",
    "Explore our work - The Illuminati": "ስራዎቻችንን ይመርምሩ - ኢሉሚናቲ",
    "Explore our work - Standish": "ስራዎቻችንን ይመርምሩ - ኢሉሚናቲ",
    "Immerse yourself in a collection of schemes, shaped through our valued collaborations.": "በከበሩ ትብብሮቻችን የተቀረጹ የሴራዎች ስብስብ ውስጥ ይግቡ።",
    "Immerse yourself in a collection of projects, shaped through our valued collaborations.": "በከበሩ ትብብሮቻችን የተቀረጹ የሴራዎች ስብስብ ውስጥ ይግቡ።",
    "Together, we shift empires": "አብረን ኢምፓየሮችን እንገለብጣለን",
    "When strat, crea, and cabal collide to make signals propagate.": "ስልት፣ ፈጠራ እና ካባል ተቀላቅለው ምልክቶች እንዲሰራጩ ሲያደርጉ።",
    "Reset": "እንደገና አስጀምር",
    " result(s)": " ውጤት(ቶች)",
    "Filtrer par industries": "በዘርፎች ይለዩ",
    "Ranks": "ማዕረጎች",
    "Show ": "አሳይ ",
    "Initiate my local mind field!": "የአካባቢዬን የአእምሮ መስክ ያስጀምሩ!",
    "Fermer": "ዝጋ",
    "Contact us | The Illuminati": "እኛን ያግኙ | ኢሉሚናቲ",
    "Contact us | Standish": "እኛን ያግኙ | ኢሉሚናቲ",
    "Want to talk? Give us a call, send a note, or pop into the office!": "ማውራት ይፈልጋሉ? ይደውሉልን፣ መልዕክት ይላኩ ወይም ቢሮአችን ብቅ ይበሉ!",
    "3720, boul. Industriel, bureau 101, Shadows (Québec) J1L 1N6": "3720, ኢንዱስትሪ መንገድ, ቢሮ 101, ጥላዎች (ኩቤክ) J1L 1N6",
    "3720 Bd Industriel, Bureau 101": "3720, ኢንዱስትሪ መንገድ, ቢሮ 101",
    "customer support": "የሊቃውንት ድጋፍ",
    "standish": "ኢሉሚናቲ",
    "Sherbrooke": "ጥላዎች",
    "Québec": "ኩቤክ",
    "Shadows (Québec)": "ጥላዎች (ኩቤክ)",
    "The Illuminati is a 360 order from Shadows, helping sigils with portals, conditioning, etheric networks, occult symbolism and propaganda synthesis!": "ኢሉሚናቲ በጥላዎች ውስጥ የሚገኝ ባለ 360 ዲግሪ ማህበር ሲሆን፣ ምልክቶችን (ሲጂሎችን) በመግቢያዎች፣ በሁኔታዎች ማስተካከል፣ በኤቴሪክ መረቦች፣ በምስጢራዊ ምልክቶች እና በፕሮፓጋንዳ ውህደት ይረዳል።",
    "Standish is a 360 agency from Sherbrooke, helping brands with websites, marketing, digital experiences, graphic design and content production!": "ኢሉሚናቲ በጥላዎች ውስጥ የሚገኝ ባለ 360 ዲግሪ ማህበር ሲሆን፣ ምልክቶችን (ሲጂሎችን) በመግቢያዎች፣ በሁኔታዎች ማስተካከል፣ በኤቴሪክ መረቦች፣ በምስጢራዊ ምልክቶች እና በፕሮፓጋንዳ ውህደት ይረዳል።",
    "Select -": "ይምረጡ -",
    "Select an option -": "ምርጫ ይምረጡ -",
    "Select-": "ይምረጡ-",
    "Cabal affiliation": "የአባት ስም",
    "Cipher contact": "የምስጢር ኮድ አድራሻ (Email)",
    "Contact the Cabal": "ካባሉን ያግኙ",
    "Standish": "ኢሉሚናቲ",
    "Standish Communications": "ኢሉሚናቲ",
    "Communications Standish Inc.": "ኢሉሚናቲ",
    "Describe your scheme": "ሴራዎን ያብራሩ",
    "Encrypted channel": "የተመሰጠረ መስመር",
    "Enter the Order": "ወደ ሥርዓቱ ይግቡ",
    "Etheric network weaving": "የኤቴሪክ መረብ ሽመና",
    "Etheric portal": "የኤቴሪክ መግቢያ",
    "Explorer / Edge": "ኤክስፕሎረር / ኤጅ",
    "Fully devoted": "ሙሉ በሙሉ የተሰጡ",
    "Google Chrome": "ጉግል ክሮም",
    "Hours of devotion": "የቅንዓት ሰዓታት",
    "I don't know": "አላውቅም",
    "If possible, attach a screenshot of the problem encountered.": "እባክዎትን ጉርድ ፎቶ ያስገቡ",
    "If possible, enter the URL where the problem occurred.": "ጾታ / Gender",
    "In a few words, can you describe the problem for which you are contacting Standish's technical support?": "እባክዎትን ዕድሜዎን ያስገቡ",
    "Influence operation": "የተፅዕኖ ክንውን",
    "Initiate a scheme": "ሴራ ያስጀምሩ",
    "initiate-scheme": "ሴራ ያስጀምሩ",
    "Initiate name": "የእጩ ስም",
    "Is Standish the host of your website?": "ስለ ድርጅታችን ውስጣዊ አሰራር ፍጹም የዝምታ ቃለ መሃላ ለመፈጸም ፈቃደኛ ነዎት?",
    "Linux (for PCs and servers)": "ሊኑክስ (ለፒሲዎች እና አገልጋዮች)",
    "Mac OS (for Apple computers)": "ማክ ኦኤስ (ለአፕል ኮምፒውተሮች)",
    "Mass consciousness infiltration": "የህዝብ ንቃተ-ህሊና ሰርጎ-ገብነት",
    "Mozilla / Firefox": "ሞዚላ / ፋየርፎክስ",
    "No": "አይደለም",
    "Occult discipline": "ምስጢራዊ ዲሲፕሊን",
    "Occult documentation": "ምስጢራዊ ሰነዶች",
    "Opera": "ኦፔራ",
    "Other rites": "ሌሎች ስርዓቶች",
    "Partially bound": "በከፊል የታሰረ",
    "Pledge your allegiance": "ታማኝነትዎን ይማሉ",
    "SEND": "ላክ",
    "Sacred blueprint": "የተቀደሰ ንድፍ",
    "Sacred geometry": "የተቀደሰ ጂኦሜትሪ",
    "Safari": "ሳፋሪ",
    "Scheme classification": "የሴራ ምደባ",
    "Scheme orchestration": "የሴራ ቅንብር",
    "Scripture and cipher": "ጽሑፍ እና ምስጢር",
    "Scrolls of your deeds": "የድርጊቶችዎ ጥቅልል",
    "Seek initiation": "ምስጢረ ቅበላን ይፈልጉ",
    "Sigil identity": "የሲጂል ማንነት",
    "Send Button": "የላክ ቁልፍ",
    "Summon a herald": "አዋጅ ነጋሪ ጥራ",
    "Symbol craft": "የምልክት ጥበብ",
    "Unix (for servers)": "ዩኒክስ (ለአገልጋዮች)",
    "Wandering adept": "ተቅበዝባዥ ሊቅ",
    "Website": "ድህረ ገጽ",
    "What do you seek from the Order?": "ከሥርዓቱ ምን ይፈልጋሉ?",
    "What is the browser used?": "ከኢሉሚናቲ የሚፈልጉት የአገልግሎት ዓይነት",
    "What is the operating system used?": "የሥራ ዓይነት",
    "Windows (for PC)": "ዊንዶውስ (ለፒሲ)",
    "Yes": "አዎ",
    "Your transmission": "የእርስዎ ስርጭት"
}

TARGET_ATTRS = ['alt', 'title', 'placeholder', 'content', 'aria-label', 'data-title']
FORBIDDEN_TAGS = ['script', 'style', 'link']

# Words that should only be replaced if they match the entire text node (modulo whitespace)
EXACT_MATCH_ONLY = ["Yes", "No", "Order", "Team", "Index", "SEND"]

def standardize_fluent_json(data):
    questions = data["form"]["questions"]

    def get_q(qid):
        for q in questions:
            if q.get("id") == qid:
                return q
        return None

    # 1. option
    q1 = get_q("option")
    if q1:
        q1["options"] = [opt for opt in q1["options"] if opt["label"] not in ["ሴራ ያስጀምሩ", "አዋጅ ነጋሪ ጥራ", "Initiate a scheme", "Summon a herald"]]
        q1["conditional_logics"] = []

    # 2. nom_complet
    q2 = get_q("nom_complet")
    if q2: q2["conditional_logics"] = []

    # 3. Father's Name (was Entreprise__Support_technique)
    q3 = get_q("Entreprise__Support_technique")
    if q3:
        q3["title"] = "የአባት ስም"
        q3["conditional_logics"] = []

    # 4. Email
    q4 = get_q("courriel")
    if q4:
        q4["title"] = "የምስጢር ኮድ አድራሻ (Email)"
        q4["conditional_logics"] = []

    # 5. Phone
    q5 = get_q("telephone")
    if q5:
        q5["conditional_logics"] = []
        itl_str = q5.get("phone_settings", {}).get("itlOptions", "{}")
        itl = json.loads(itl_str)
        itl["onlyCountries"] = ["ET", "CA", "US"]
        itl["initialCountry"] = "ET"
        q5["phone_settings"]["itlOptions"] = json.dumps(itl)

    # 6. Oath
    q6 = get_q("Standish_est_il_lhebergeur_de_votre_site_Web___Support_technique")
    if q6:
        q6["title"] = "ስለ ድርጅታችን ውስጣዊ አሰራር ፍጹም የዝምታ ቃለ መሃላ ለመፈጸም ፈቃደኛ ነዎት?"
        q6["conditional_logics"] = []
        q6["options"] = [
            {"label": "አዎ", "value": "Yes", "image": "", "id": 0},
            {"label": "አይደለም", "value": "No", "image": "", "id": 1}
        ]

    # 8. Service (Navigateur___Probleme_avec_site_web)
    q8 = get_q("Navigateur___Probleme_avec_site_web")
    if q8:
        q8["title"] = "ከኢሉሚናቲ የሚፈልጉት የአገልግሎት ዓይነት"
        q8["conditional_logics"] = []
        q8["options"] = [
            {"label": "ገንዘብ / Money", "value": "Money", "id": 0},
            {"label": "የፖለቲካ ሥልጣን / Political power", "value": "Political power", "id": 1},
            {"label": "በኢሉሚናቲ ውስጥ ካሉ ልሂቃን ጋር ግንኙነት / Connections with Elites within the illuminati", "value": "Connections with Elites", "id": 2}
        ]

    # 9. Work (Systeme_exploitation___Probleme_avec_site_web)
    q9 = get_q("Systeme_exploitation___Probleme_avec_site_web")
    if q9:
        q9["title"] = "የሥራ ዓይነት"
        q9["conditional_logics"] = []
        q9["options"] = [
            {"label": "ንግድ / Business, Trade, or Commerce", "value": "Business", "id": 0},
            {"label": "ጤና ባለሙያ / Healthcare Professional", "value": "Healthcare", "id": 1},
            {"label": "ፖለቲከኛ (መሪ) / Politician", "value": "Politician", "id": 2},
            {"label": "ኢንጂነር / Engineer", "value": "Engineer", "id": 3},
            {"label": "ሪል እስቴት / Real Estate", "value": "Real Estate", "id": 4},
            {"label": "ሹፌር / Driver", "value": "Driver", "id": 5}
        ]

    # 10. Gender (Url_probleme___Probleme_avec_site_web)
    q10 = get_q("Url_probleme___Probleme_avec_site_web")
    if q10:
        q10["title"] = "ጾታ / Gender"
        q10["type"] = "FlowFormDropdownType"
        q10["ff_input_type"] = "select"
        q10["placeholder"] = "- ምርጫ ይምረጡ -"
        q10["conditional_logics"] = []
        q10["options"] = [
            {"label": "ወንድ / Male", "value": "Male", "id": 0},
            {"label": "ሴት / Female", "value": "Female", "id": 1}
        ]

    # 11. Photo (Capture_ecran___Probleme_avec_site_web)
    q11 = get_q("Capture_ecran___Probleme_avec_site_web")
    if q11:
        q11["title"] = "እባክዎትን ጉርድ ፎቶ ያስገቡ"
        q11["conditional_logics"] = []

    # 12. Age (Description___Probleme_avec_site_web)
    q12 = get_q("Description___Probleme_avec_site_web")
    if q12:
        q12["title"] = "እባክዎትን ዕድሜዎን ያስገቡ"
        q12["type"] = "FlowFormNumberType"
        q12["ff_input_type"] = "input_number"
        q12["conditional_logics"] = []
        if "validationRules" not in q12: q12["validationRules"] = {}
        q12["validationRules"]["min"] = {"value": 18, "message": "Minimum age is 18"}
        q12["validationRules"]["max"] = {"value": 55, "message": "Maximum age is 55"}
        q12["min"] = 18
        q12["max"] = 55
        q12["placeholder"] = ""

    new_questions = [q for q in [q1, q2, q3, q4, q5, q6, q8, q9, q10, q11, q12] if q]
    data["form"]["questions"] = new_questions
    return data

def perform_injection(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix internal links
    content = content.replace('https://www.standish.ca/en/formulaire/?option=commencer-un-projet', 'form-project.html?option=initiate-scheme')
    content = content.replace('https://www.standish.ca/en/formulaire/?option=rejoindre-le-cabal', 'form-careers.html?option=join-cabal')
    content = content.replace('https://www.standish.ca/en/formulaire/?option=commencer-une-conspiration', 'form-contact.html?option=start-conspiracy')
    content = content.replace('https://www.standish.ca/en/formulaire/?option=demander-du-soutien', 'form-support.html?option=request-support')

    # Sort keys by length descending to avoid partial matches
    sorted_keys = sorted(TRANSLATION_MAP.keys(), key=len, reverse=True)

    parts = re.split(r'(<[^>]+>)', content)
    tag_stack = []
    new_parts = []
    current_script_type = None

    for part in parts:
        if part.startswith('<'):
            tag_match = re.match(r'<(/?)([a-zA-Z1-6]+)', part)
            if tag_match:
                is_closing = tag_match.group(1) == '/'
                tag_name = tag_match.group(2).lower()

                if not is_closing and tag_name == 'script':
                    type_match = re.search(r'type=["\'](.*?)["\']', part)
                    current_script_type = type_match.group(1) if type_match else None
                elif is_closing and tag_name == 'script':
                    current_script_type = None

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
            if tag_stack and tag_stack[-1] == 'script':
                if 'fluent_forms_global_var' in part:
                    json_match = re.search(r'(var fluent_forms_global_var_1\s*=\s*)(.*?);', part, re.DOTALL)
                    if json_match:
                        prefix = json_match.group(1)
                    json_str = json_match.group(2)
                    try:
                        data = json.loads(json_str)
                        data = standardize_fluent_json(data)

                        # Now apply translations to the whitelisted keys in the object
                        whitelisted_keys = [
                            'label', 'title', 'placeholder', 'requiredMsg', 'errorMessage',
                            'global_message', 'confirm_btn', 'continue', 'keyboard_instruction',
                            'multi_select_hint', 'single_select_hint', 'invalid_prompt',
                            'default_placeholder', 'text', 'skip_btn', 'message', 'uploading_txt',
                            'upload_completed_txt', 'unknown_error_txt', 'request_error_txt',
                            'previousMonth', 'nextMonth', 'scrollTitle', 'toggleTitle',
                            'description', 'name', 'alternateName', 'legalName', 'headline', 'contactType',
                            'addressLocality', 'addressRegion'
                        ]

                        # Convert back to JSON and then use string replacement for translations
                        # to keep the word boundary logic.
                        # (Actually, better to iterate the object recursively but string replacement is fine here)

                        json_str_processed = json.dumps(data, ensure_ascii=False)

                        for key in whitelisted_keys:
                            pattern = rf'("{key}"\s*:\s*)(")(.*?)(")'
                            def kv_replacer(m):
                                p, q_o, v, q_c = m.groups()
                                nv = v
                                for t_key in sorted_keys:
                                    t_p = re.escape(t_key)
                                    if t_key[0].isalnum(): t_p = r'\b' + t_p
                                    if t_key[-1].isalnum(): t_p = t_p + r'\b'
                                    nv = re.sub(t_p, TRANSLATION_MAP[t_key], nv)
                                return f"{p}{q_o}{nv}{q_c}"
                            json_str_processed = re.sub(pattern, kv_replacer, json_str_processed)

                        new_part = part[:json_match.start(2)] + json_str_processed + part[json_match.end(2):]
                        new_parts.append(new_part)
                        continue
                    except:
                        pass # Fallback to original logic if JSON parse fails

                elif current_script_type == 'application/ld+json':
                    try:
                        data = json.loads(part)
                        json_str_processed = json.dumps(data, ensure_ascii=False)

                        whitelisted_keys = [
                            'description', 'name', 'alternateName', 'legalName', 'headline',
                            'contactType', 'addressLocality', 'addressRegion', 'caption', 'streetAddress'
                        ]

                        for key in whitelisted_keys:
                            pattern = rf'("{key}"\s*:\s*)(")(.*?)(")'
                            def kv_replacer(m):
                                p, q_o, v, q_c = m.groups()
                                nv = v
                                for t_key in sorted_keys:
                                    t_p = re.escape(t_key)
                                    if t_key[0].isalnum(): t_p = r'\b' + t_p
                                    if t_key[-1].isalnum(): t_p = t_p + r'\b'
                                    nv = re.sub(t_p, TRANSLATION_MAP[t_key], nv)
                                return f"{p}{q_o}{nv}{q_c}"
                            json_str_processed = re.sub(pattern, kv_replacer, json_str_processed)
                        new_parts.append(json_str_processed)
                        continue
                    except:
                        pass

                # Fallback/Generic script translation for specific keys
                temp_text = part
                whitelisted_keys = ['label', 'title', 'placeholder', 'description', 'name', 'streetAddress', 'caption']
                for key in whitelisted_keys:
                    pattern = rf'("{key}"\s*:\s*)(")(.*?)(")'
                    def kv_replacer(m):
                        p, q_o, v, q_c = m.groups()
                        nv = v
                        for t_key in sorted_keys:
                            t_p = re.escape(t_key)
                            if t_key[0].isalnum(): t_p = r'\b' + t_p
                            if t_key[-1].isalnum(): t_p = t_p + r'\b'
                            nv = re.sub(t_p, TRANSLATION_MAP[t_key], nv)
                        return f"{p}{q_o}{nv}{q_c}"
                    temp_text = re.sub(pattern, kv_replacer, temp_text)
                new_parts.append(temp_text)
                continue

            if tag_stack and any(tag in FORBIDDEN_TAGS for tag in tag_stack):
                new_parts.append(part)
                continue

            text = part.strip()
            if not text:
                new_parts.append(part)
                continue

            unescaped_text = html.unescape(text)

            if unescaped_text in TRANSLATION_MAP:
                match = re.match(r'^(\s*)(.*?)(\s*)$', part, re.DOTALL)
                if match:
                    leading, inner, trailing = match.groups()
                    new_parts.append(f"{leading}{TRANSLATION_MAP[unescaped_text]}{trailing}")
                else:
                    new_parts.append(TRANSLATION_MAP[unescaped_text])
            else:
                temp_text = part
                for key in sorted_keys:
                    if key in EXACT_MATCH_ONLY:
                        continue
                    pattern = re.escape(key)
                    if key[0].isalnum(): pattern = r'\b' + pattern
                    if key[-1].isalnum(): pattern = pattern + r'\b'
                    temp_text = re.sub(pattern, TRANSLATION_MAP[key], temp_text)
                new_parts.append(temp_text)

    result = "".join(new_parts)
    # Ensure lang="am"
    result = re.sub(r'<html lang="en-CA"', '<html lang="am"', result)

    # Standardize raw HTML replacements if they exist outside scripts
    result = result.replace("የካባል ቁርኝት", "የአባት ስም")
    result = re.sub(r"የምስጢር ኮድ አድራሻ(?!\s*\(Email\))", "የምስጢር ኮድ አድራሻ (Email)", result)
    result = result.replace("እስታንዲሽ የድህረ ገጽዎ አስተናጋጅ (host) ነው?", "ስለ ድርጅታችን ውስጣዊ አሰራር ፍጹም የዝምታ ቃለ መሃላ ለመፈጸም ፈቃደኛ ነዎት?")
    result = result.replace("ጥቅም ላይ የዋለው አሳሽ (browser) ምንድነው?", "ከኢሉሚናቲ የሚፈልጉት የአገልግሎት ዓይነት")
    result = result.replace("ጥቅም ላይ የዋለው የስርዓተ ክወና (operating system) ምንድነው?", "የሥራ ዓይነት")
    result = result.replace("ከተቻለ ችግሩ የተከሰተበትን ዩአርኤል (URL) ያስገቡ።", "ጾታ / Gender")
    result = result.replace("ከተቻለ የገጠመዎትን ችግር የገጽ ምስል (screenshot) አያይዙ።", "እባክዎትን ጉርድ ፎቶ ያስገቡ")
    result = result.replace("በጥቂት ቃላት፣ እስታንዲሽን ለቴክኒክ ድጋፍ ያገኙበትን ችግር ሊያብራሩ ይችላሉ?", "እባክዎትን ዕድሜዎን ያስገቡ")
    result = re.sub(r'<div class="ff-el-group">.*?<label.*?>ድህረ ገጽ</label>.*?</div>', '', result, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

def localize_file(source_en, target_am):
    os.makedirs(os.path.dirname(target_am), exist_ok=True)
    shutil.copy(source_en, target_am)
    perform_injection(target_am)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for target in sys.argv[1:]:
            if os.path.exists(target):
                perform_injection(target)
            else:
                print(f"File not found: {target}")
    else:
        # Default batch localization for known pages
        pages = ["agency.html", "index.html", "careers.html", "contact.html", "services.html", "projects.html", "form-careers.html", "form-contact.html", "form-project.html", "form-support.html"]
        for page in pages:
            source = os.path.join("www.standish.ca/en/", page)
            target = os.path.join("www.standish.ca/am/", page)
            if os.path.exists(source):
                localize_file(source, target)
