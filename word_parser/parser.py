import json
import os
import re

PATH = os.path.dirname(__file__)

class Parser(object):
    language_names = {
        "Gàidhlig": ["gaidhlig", "scottish gaelic"]
    }

    def __init__(self, language:str) -> None:
        self.language_aliases = {alias.lower(): name for name, aliases in self.language_names.items() for alias in aliases}
        self.language = language
        self._rules = None

    @property
    def language(self) -> str: return self._language

    @language.setter
    def language(self, language:str) -> None:
        if language in self.language_names:
            self._language = language
        else:
            self._language = self.language_aliases[language.lower()]         

    @property
    def rules(self):
        if not self._rules:
            rules_path = os.path.join(PATH, self.language, "graphemes.json")
            with open(rules_path) as f:
                self._rules = json.load(f)
        return self._rules

    def to_ipa(self, word:str) -> str:
        rules = self.rules
        graphemes = sorted(rules, key=lambda g:len(g), reverse=True)
        pattern = f"({'|'.join(graphemes)})"
        parts = re.findall(pattern, word)

        ipa = []
        for idx, part in enumerate(parts):
            rule = rules[part]
            val = self.eval_pattern(rule["patterns"], word)


        return

    @staticmethod
    def eval_pattern(patterns, word):
        for pattern in patterns:
            

    def __repr__(self): return f"{self.language} Parser"


parser = Parser("gaidhlig")

test = "bean"
parser.to_ipa(test)

print("done")