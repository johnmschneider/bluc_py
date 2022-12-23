def matchesAny(str, thingsToMatch):
    for matchThis in thingsToMatch:
        if str == matchThis:
            return True
    return False