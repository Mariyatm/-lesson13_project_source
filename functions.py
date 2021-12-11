def is_tag(word):
    return word.startswith("#")


def get_tag(word):
    return word.replace("#","").replace("!","")