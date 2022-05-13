from list_keywords import KEYWORDS, NUMBERS
from definition import *
import re

# transform "IF" in current language "if", "si", etc...
def translate(keyword_lang, keywords_level):
    if type(keywords_level) == str:
        if keywords_level in keyword_lang:
            trad = keyword_lang[keywords_level]
        else:
            trad = keywords_level

        trad_compile = re.compile(trad)
        if trad_compile.groups != 1 :
            trad = "(" + trad + ")"
        return trad

    elif type(keywords_level) == list :
        L = []
        for sub in keywords_level:
            L.append(translate(keyword_lang,sub))
        return L
    elif type(keywords_level) == dict:
        D = {}
        for key in keywords_level.keys():
            D[key] = translate(keyword_lang,keywords_level[key])
        return D





# After the level 4
# so what is not in quotes is code,
# and any keyword in the code can be colored independently
# of what is around it, so we use a general function
# This general function uses 2 constants KEYWORDS and NUMBERS

def rule_all(level):


    # get keyword by level
    keyword_by_level = KEYWORDS[level]

    list_rules = []

    # Rule for comments :
    list_rules.append( { 'regex': '#.*$', 'token': 'comment', 'next': 'start' } )

    # Rule for quoted string :
    list_rules.append( { 'regex': '\"[^\"]*\"', 'token': 'constant.character', 'next': 'start' } )

    list_rules.append( { 'regex': "\'[^\']*\'", 'token': 'constant.character', 'next': 'start' } )

    # Rule for blanks marks :
    list_rules.append( { 'regex': '_\\?_', 'token': 'invalid', 'next': 'start' })
    list_rules.append( { 'regex': '(^| )(_)(?= |$)', 'token': ['text','invalid'], 'next': 'start' } )


    # Rules for numbers
    if (NUMBERS[level]["number"]) :
        if (NUMBERS[level]["number_with_decimal"]) :
            number_regex = '([0-9]*\\.?[0-9]+)'
        else:
            number_regex = '([0-9]+)'

        list_rules.append({'regex': START_WORD + number_regex + END_WORD, 'token': ['text','variable'], 'next':'start'} )

        # Special case of an number directly followed by a number 
        for command in keyword_by_level["SP_K"]: 
            list_rules.append({
                'regex': START_WORD + K(command) + number_regex + END_WORD,
                'token': ['text','keyword','variable'],
                'next': 'start',
            })

        for command in keyword_by_level["K"]:
            list_rules.append({
                'regex': K(command) + number_regex + END_WORD,
                'token': ['keyword','variable'],
                'next': 'start',
            })


    # Rules for commands of SP_K_SP 
    # These are the keywords that must be "alone" so neither preceded nor followed directly by a word 
    for command in keyword_by_level["SP_K_SP"]:
        list_rules.append({
            'regex': START_WORD + K(command) + END_WORD,
            'token': ["text","keyword"],
            'next': "start", 
        })
    

    # Rules for commands of K 
    #  These are the keywords that are independent of the context (formerly the symbols
    # In particular, even if they are between 2 words, the syntax highlighting will select them
    for command in keyword_by_level["K"]:
        list_rules.append({
            'regex': K(command),
            'token': "keyword",
            'next': "start", 
        })

    # Rules for commands of SP_K 
    #  This category of keywords allows you to have keywords that are not preced
    # by another word, but that can be followed immediately by another word. (see the PR #2413)*/
    for command in keyword_by_level["SP_K"]:
        list_rules.append({
            'regex': START_WORD + K(command),
            'token': ["text","keyword"],
            'next': "start", 
        })

    # Rules for commands of K_SP 
    #  This category of keywords allows you to have keywords that can be preceded immediate
    # by another word, but that are not followed by another word.*/
    for command in keyword_by_level["K_SP"]:
        list_rules.append({
            'regex': K(command) + END_WORD,
            'token': "keyword",
            'next': "start", 
        })

    return {"start" :list_rules}

