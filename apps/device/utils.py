"""
bbofuser:device
FILE: utils
Created: 8/3/15 6:00 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

import re
import random
from django.conf import settings


def get_phrase(count=2):
    # Build a phrase
    f = open(settings.WORD_LIST)

    sentence = [x.strip() for x in f.readlines()]
    if settings.DEBUG:
        print("Sentence:", sentence)

    words = []

    for line in sentence:
        word = line.split(' ')
        if word != "":
            words += word

    if settings.DEBUG:
        print("Words:", words)

    phrase = '-'.join(random.choice(words) for i in range(count)).lower()
    phrase = phrase.replace("'", "")
    phrase = phrase + str(random.randint(1, 9999))

    if settings.DEBUG:
        print(count, "word phrase:", phrase)
    return phrase