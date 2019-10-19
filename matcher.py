"""
Idea: start with a subset of regexp language and climb all the way up to a fully featured regexp language

Subset 1:
- identity matching for a-zA-Z
- star operator for a single character(a-zA-Z.) --> a*
- . character to indicate any a-zA-Z

Strategy
- Given a pattern convert "tokenize" it so that we can clearly distinguish each piece of matching logic we should apply
- Define the matching logic for our three "operators"(matching a-zA-Z,matching ., star operator )
- Navigate the tokenized pattern and apply the different checking pieces of logic
"""
from matching_operators import match_identity, match_star, match_plus


def generate_star_token(value):
    return {
        'type': 'star',
        'value': value
    }


def generate_identity_token(value):
    return {
        'type': 'identity',
        'value': value
    }


def generate_plus_token(value):
    return {
        'type': 'plus',
        'value': value
    }


def tokenize(pattern):
    """
    Tokenizes a pattern for our regexp subset into a list of dicts to be used to apply the different pieces of checking logic
    required to match an input string with the pattern
    :param pattern: The pattern to tokenize
    :return: A list of tokens(dicts)


    >>> tokenize("ab*")
    [{'type': 'identity', 'value': 'a'}, {'type': 'star', 'value': 'b'}]

    >>> tokenize("abc*af*")
    [{'type': 'identity', 'value': 'ab'}, {'type': 'star', 'value': 'c'}, {'type': 'identity', 'value': 'a'}, {'type': 'star', 'value': 'f'}]

    >>> tokenize("abc")
    [{'type': 'identity', 'value': 'abc'}]
    """

    tokens = []
    last_identity_token_value = []

    for i, char in enumerate(pattern):
        if i < len(pattern) - 1:
            if pattern[i + 1] in ['*', '+']:
                if last_identity_token_value:
                    tokens.append(generate_identity_token(''.join(last_identity_token_value)))
                    last_identity_token_value = []
                if pattern[i + 1] == '*':
                    token = generate_star_token(char)
                else:
                    token = generate_plus_token(char)
                tokens.append(
                    token
                )
                continue
        if char not in ['*', '+']:
            last_identity_token_value.append(
                char
            )
    if last_identity_token_value:
        tokens.append(generate_identity_token(''.join(last_identity_token_value)))
    return tokens


def matcher(string, pattern):
    """
    Matches a string with a pattern the uses our subset of the regepx language
    :param string: The string to match
    :param pattern: The pattern to match
    :return: if a match was found

    >>> matcher("pippo", "pip*o")
    True

    >>> matcher("random", "random!*")
    True

    >>> matcher("random", "!*rand*oma*")
    True

    >>> matcher("random", "!*rand.*")
    True

    >>> matcher("random", "ra.*p.*")
    False

    >>> matcher("ddasdl", "d+.*")
    True
    """

    tokenized_pattern = tokenize(pattern)
    analyzed_len = 0
    for token in tokenized_pattern:
        token_type = token['type']
        token_value = token['value']
        if analyzed_len == len(string):
            return token_type == 'star'
        if token_type == 'identity':
            result = match_identity(string[analyzed_len:len(token_value) + analyzed_len], token_value)
            if not result:
                return False
            analyzed_len += len(token_value)
        elif token_type == 'star':
            found_occurrences = match_star(string[analyzed_len:], token_value)
            analyzed_len += found_occurrences
        elif token_type == 'plus':
            result, found_occurrences = match_plus(string[analyzed_len:], token_value)
            if not result:
                return False
            analyzed_len += found_occurrences
    return analyzed_len == len(string)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
