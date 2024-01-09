from rich.text import Text
from rich.console import Console
import random
import itertools

import logic
# standard logical equivalences
# (A ∧ B) ≡ (B ∧ A) commutativity of ∧
# (A ∨ B) ≡ (B ∨ A) commutativity of ∨
# ((A ∧ B) ∧ C) ≡ (A ∧ (B ∧ C)) associativity of ∧
# ((A ∨ B) ∨ C) ≡ (A ∨ (B ∨ C)) associativity of ∨
# ¬(¬A) ≡ A double negation elimination


p00 = '(((A ∨ B) → C) ∧ (D ∧ (¬E)))'


class KB:
    def __init__(self):
        self.model = {}
        self.symbols = set()
        self.sentences = []

    def tell(self, sentence):
        for sym in sentence.get_symbol_list():
            self.symbols.add(sym)
        self.sentences.append(sentence)

    def ask(self, sentence):
        if sentence.is_atomic() and sentence.name.startswith('V'):
            return sentence in self.symbols
        if sentence.is_atomic() and sentence.name.startswith('A'):
            return True
            pass


    def inference(self):
        pass


