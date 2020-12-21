import argparse
from typing import Dict, Set, Iterable


import nltk
from nltk.corpus import words

nltk.download("words")

sample_spell_list = \
[
    "Eldritch Blast",
    "Green Flame Blade",
    "Prestidigitation",
    "Bless",
    "Mage Armor",
    "Distort Value",
    "Earth bind",
    "Find Familiar",
    "Hold Person",
    "Misty Step",
    "Shatter",
    "Sleep"
]


def get_single_replacements(spell_name: str, valid_tokens: Set[str]) -> Iterable[str]:
    lower_spell_name = spell_name.lower()
    spell_tokens = [token for token in lower_spell_name.split(" ")] # These tokens should be assumed to exist even if not in the corpus\

    for character_index in range(len(lower_spell_name)):
        for ascii_index in range(21,126): # punctuation, letters, spaces
            variant_name = lower_spell_name[:character_index] + chr(ascii_index) + lower_spell_name[(character_index+1):]
            if (variant_name == lower_spell_name): 
                continue
            tokens = [token for token in variant_name.split(" ")]
            if all([token in valid_tokens or token in spell_tokens for token in tokens]):
                yield(variant_name)

def print_header(text: str):
    """
    Pretty-print the input text
    """
    print("=" * len(text))
    print(text)
    print("-" * len(text))


def print_replacements_for_list(spell_list: Iterable[str], valid_tokens: Set[str]):
    """
    Pretty-print all the Ring of the Grammarian permutations of the 
    """
    for spell_name in spell_list:
        print_header(spell_name)
        for spell_name_variant in get_single_replacements(spell_name, valid_tokens):
            print(spell_name_variant)
        print("")

def get_argument_parser():
    parser = argparse.ArgumentParser(description="Find all the permutations of spells allowed by the Ring of the Grammarian")
    parser.add_argument('spells', metavar='S', type=str, nargs='+', help='the names of spells to permute')
    return parser

if __name__ == "__main__":
    spells = get_argument_parser().parse_args().spells
    print(spells)
    print_replacements_for_list(sample_spell_list, set(words.words()))