from string import ascii_uppercase, ascii_lowercase, digits
from random import choice
from constance import config


def short_link_generator():
    size = config.LENGTH
    chars = str()

    if config.LOWERCASE:
        chars += ascii_lowercase
    if config.DIGITS:
        chars += digits
    if config.UPPERCASE:
        chars += ascii_uppercase

    url = ''.join(choice(chars) for _ in range(size))

    return url
