import re

pattern = r"([/[][^[\]/]+[/\]])"

text = """
(North Wales, standard) IPA(key): /ˈei̯sɔɨ̯s/
(North Wales, colloquial) IPA(key): /ˈei̯ʃɔɨ̯s/
(South Wales, standard) IPA(key): /ˈei̯sɔi̯s/
(South Wales, colloquial) IPA(key): /ˈei̯ʃɔi̯s/, /ˈei̯ʃɔs/, /ˈei̯ʃʊs/, /ˈiːʃʊs/, /ˈɪʃʊs/
"""

matches = re.findall(pattern, text)
print(" ".join(matches))