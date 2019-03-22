# -*- coding: utf-8 -*-
"""

NLPAssignment4.py

Author : jayaramakapil
"""
import os
import re
import copy
from collections import Counter
from collections import defaultdict

def Sentences(Inputfile):
    """
    This function creates strings of each sentence in a list

    """
    global str_list
    with open(Inputfile, 'r+') as f:
        data = f.read()
        blacklist = ["(: --)", "(TOP (. .))", "(SBAR (-NONE- 0)", "(. ?)", "-LRB-", "-RRB-", "(' ')", "(: ;)",
                     "(\" \")", "(` `)", "(: :)", "(. .)", "(`` ``)", "('' '')", "(, ,)", "($ $)", "( )",
                     "(SBAR-1 (-NONE- *pseudo-attach*)))", "('' ')", "(`` `)"]
        sentences = []
        for i in blacklist:
            data = data.replace(i, '')
        data = ' '.join(data.split())
        l = data.split('(TOP END_OF_TEXT_UNIT)')
        str_list = [x.strip() for x in l if x.strip()]


def is_symbol_char(character):
    """
    This function checks if a character is Uppercase

    """
    return character.isalpha() or character in '-=$!?.'


def tokenize(characters):
    """
    This function tokenenizes words in a sentence

    """
    tokens = []

    while characters:
        character = characters.pop(0)

        if character.isspace():
            pass

        elif character == '(':
            characters, result = tokenize(characters)
            tokens.append(result)

        elif character == ')':
            break

        elif is_symbol_char(character):

            symbol = ''

            while is_symbol_char(character):
                symbol += character
                character = characters.pop(0)
            characters.insert(0, character)

            tokens.append(symbol)

    return characters, tokens


def extract_rules(tokens):
    """
    This function extracts rules from a sentence

    """
    head, *tail = tokens

    sub_rules = [x[0] for x in tail if not isinstance(x, str)]

    if len(sub_rules) != 0:
        rules_dictionary[head].append(str(sub_rules))

        # print(head, '-->', *sub_rules)

    for token in tail:
        if isinstance(token, list):
            extract_rules(token)


def extract_rules_all():
    """
    This function extracts rules from all the sentences

    """
    global rules_dictionary
    global tokens

    for string in str_list:
        characters, tokens = tokenize(list(string))
        extract_rules(tokens[0][1])


def FrequentRules(dictionary):
    """
    function for The the 10 most frequent rules regardless of the non-terminal on the left-hand side
    """
    hash_dict = {k: dict(Counter(v)) for k, v in dictionary.items()}
    frequent_tags = defaultdict(int)
    for dicts in hash_dict.values():
        for i, j in dicts.items():
            if i != "['-NONE-']":
                frequent_tags[i] += j
    top_list = sorted(frequent_tags.items(), key=lambda kv: kv[1], reverse=True)[:10]
    top_list = dict(top_list)
    print('The the 10 most frequent rules regardless of the non-terminal on the left-hand side: ')
    for k, v in top_list.items():
        print('{}: {}'.format(k, v))


def DistinctRules(dictionary):
    """
    function for The non-terminal that can have most diverse structures
    """
    alternative_rules = {}
    for k, v in dictionary.items():
        alternative_rules[k] = len(list(set(v)))
    answer = sorted(alternative_rules.items(), key=lambda kv: kv[1], reverse=True)[0]
    print(' The non-terminal that can have most diverse structures is: {}'.format(answer))


def lexicalize(tokens):
    """
    function for lexicalizing given rules
    """

    head, *tail = tokens

    children = [x[0] for x in tail if not isinstance(x, str)]

    if head == 'S':

        if 'VP' in children:
            head = 'VP'

        lexicalized_rules_dictionary[head].append(str(children))


    elif head == 'NP' and len(children) != 0:

        if 'NNP' in children:
            head = 'NNP'

        elif 'NN' in children:
            head = 'NN'


        elif 'NNS' in children:
            head = 'NNS'


        elif 'PP' in children:

            head = 'PP'
        lexicalized_rules_dictionary[head].append(str(children))


    elif head == 'VP' and len(children) != 0:

        if 'VBD' in children:
            head = 'VBD'

        elif 'NP' in children:
            head = 'VP'

        elif 'PP' in children:
            head = 'VP'

        lexicalized_rules_dictionary[head].append(str(children))

    else:

        if len(children) != 0:
            lexicalized_rules_dictionary[head].append(str(children))

    for token in tail:
        if isinstance(token, list):
            lexicalize(token)


def extract_lexicalized_rules_all():
    """
    function for extracting lexicalized rules
    """
    for string in str_list:
        characters, tokens = tokenize(list(string))
        lexicalize(tokens[0][1])


def main():
    """
    function to run all functions
    """
    global rules_dictionary
    global lexicalized_rules_dictionary
    Sentences(Inputfile='BROWN.pos.all')
    rules_dictionary = defaultdict(lambda: [])
    extract_rules_all()
    FrequentRules(dictionary=rules_dictionary)
    print('------------------------')
    DistinctRules(dictionary=rules_dictionary)
    print('------------------------')
    lexicalized_rules_dictionary = rules_dictionary.copy()
    extract_lexicalized_rules_all()
    FrequentRules(dictionary=lexicalized_rules_dictionary)
    print('------------------------')
    DistinctRules(dictionary=lexicalized_rules_dictionary)


main()