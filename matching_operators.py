def match_plus(string, matching_value):
    matches = match_star(string, matching_value)
    return matches != 0, matches

def match_star(string, matching_value):
    found_occurrences = 0
    for i, char in enumerate(string):
        if not match_identity(char, matching_value):
            return found_occurrences
        found_occurrences += 1
    return found_occurrences


def match_identity(string, matching_value):
    if matching_value == '.':
        return string != ''
    return string == matching_value
