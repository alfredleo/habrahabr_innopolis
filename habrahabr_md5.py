# coding: utf8
"""
Module to test correct and wrong answers in habrahabr
"""
import hashlib
import re

import httplib2
import bs4


__author__ = 'alfredleo@gmail.com (Alfred)'

URL_PARSE = 'http://habrahabr.ru/company/innopolis_university/blog/236647'


def test_habrahabr(local=False):
    """ Function to count right and wrong answers in the comments
    >>> print sum(test_habrahabr(True).values())
    2
    >>> print len(test_habrahabr(True))
    2
    """
    if local:
        response = open('data.in').read()
    else:
        http = httplib2.Http()
        dummy_status, response = http.request(URL_PARSE)
    soup = bs4.BeautifulSoup(response)

    statistics = dict()
    for user_comment in soup.find_all('div', class_="comment_body"):
        username = user_comment.find_next('a', class_='username').get_text()
        message = user_comment.find_next('div', class_='message').get_text()
        md5s = re.findall(r"([a-fA-F\d]{32})", message)
        # testing that user has any md5 hash so that he tried to answer
        for md5 in md5s:
            if username not in statistics.keys():
                statistics[username] = False
            # check if user answer is correct add to statistics
            if md5 == hashlib.md5(username + '09').hexdigest():
                # print username + " answered correctly"
                statistics[username] = True

    return statistics


def print_it(statistics):
    """
    Just prints out dictionary in a nice way
    :param statistics: dictionary of users correct or wrong answers
    """
    correct = sum(statistics.values())
    wrong = len(statistics) - correct
    print "{} correct answers, {} wrong ones".format(correct, wrong)


print_it(test_habrahabr())

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
