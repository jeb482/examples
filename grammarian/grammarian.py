import argparse
from typing import Dict, Set, Iterable


import nltk
from nltk.corpus import words



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
    """
    Returns an iterable of every valid English phrase which has an edit distance of exactly
    one letter from the `spell_name`. Allowable operations are ascii substitutions, not 
    deletions or insertions. Phrases are considered valid if and only if each token in the
    phrase is an element of `valid tokens`.

    Args
    ----

    spell_name: str
        The name of a spell which can be altered by the Ring of the Grammarian

    valid_tokens: Set[str]
        A list of every token recognized in the language. 
    """
    lower_spell_name = spell_name.lower()
    
    # We assert that existing tokens in the name of the spell are valid.
    # If "Tasha's hideous laughter" is a spell, then "Tasha's" is a token.
    spell_tokens = [token for token in lower_spell_name.split(" ")] 

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
    Pretty-print the input `text`
    """
    print("=" * len(text))
    print(text)
    print("-" * len(text))


def print_replacements_for_list(spell_list: Iterable[str], valid_tokens: Set[str]):
    """
    Pretty-print all the Ring of the Grammarian permutations of the spells in the list.
    """
    for spell_name in spell_list:
        print_header(spell_name)
        for spell_name_variant in get_single_replacements(spell_name, valid_tokens):
            print(spell_name_variant)
        print("")

def get_argument_parser():
    parser = argparse.ArgumentParser(description="Find all the permutations of spells allowed by the Ring of the Grammarian.")
    parser.add_argument('spells', metavar='"<Spell Name>"', type=str, nargs='+',
                         help='the names of spells to permute (put multi-word names in quotes)')
    return parser

if __name__ == "__main__":
    spells = get_argument_parser().parse_args().spells
    nltk.download("words")
    print_replacements_for_list(spells, set(words.words()))