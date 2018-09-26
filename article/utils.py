import datetime
import re

import math

# the purpose of strip_tags id to strips the html tag in the article
from django.utils.html import strip_tags

# https://www.youtube.com/watch?v=jipO3gSxfr0&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=19
# count word and get read time
def count_word(html_string):

    # first: strip the the article html tag
    word_string = strip_tags(html_string)
    #second: after striping the html tag, find all the word inside the word_string
    matching_words = re.findall(r'\w+',word_string)
    # third: count the all the words inside the matching_words
    count = len(matching_words)
    # return the result after counts all the words.
    return count

def get_read_time(html_string):

    # use the count_word function to count the words inside the article
    count = count_word(html_string)
    # math.ceil mean round the number into integer whenever there is any decimal point
    # and assuming 200 word per min reading
    read_time_min = math.ceil(count/200)
    # turn the read_time_min into integer
    return int(read_time_min)
