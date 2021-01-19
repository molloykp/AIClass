""" Simple unit tests for text_gen functions. 

Author: Nathan Sprague
Version: 1/10/20
"""

import unittest
import text_gen
import sys

import argparse
from unittest_utils import *


class TestNGrams(unittest.TestCase):
    def setUp(self):
        self.unigrams = {'i': 0.4, 'am': 0.2, 'think': 0.2, 'therefore': 0.2}
        self.bigrams = {'i':  {'am': 0.25, 'think': 0.75},
                        None: {'i': 1.0},
                        'am': {'i': 1.0},
                        'think': {'i': 0.5, 'therefore': 0.5},
                        'therefore': {'i': 1.0}}
        self.trigrams = {('think', 'i'): {'think': 1.0},
                         ('i', 'am'): {'i': 1.0},
                         (None, None): {'i': 1.0},
                         ('therefore', 'i'): {'am': 1.0},
                         ('think', 'therefore'): {'i': 1.0},
                         ('i', 'think'): {'i': 0.5, 'therefore': 0.5},
                         (None, 'i'): {'think': 1.0},
                         ('am', 'i'): {'think': 1.0}}

    # Unigram Tests ------------
    @points_decor(points=10, autograder_name='unigrams')
    def test_calculate_unigrams(self):
        unigrams = text_gen.calculate_unigrams(['i', 'think', 
                                                'therefore', 'i', 'am'])
        self.assertEqual(unigrams, self.unigrams)
        #self.assertEqual(0,1,'Unigram distribution did not match')

    # Bigram Tests ------------
    @points_decor(points=5, autograder_name='bigrams')
    def test_calculate_bigrams(self):
        bigrams = text_gen.calculate_bigrams(['i', 'think', 'therefore', 
                                               'i', 'am', 'i', 'think', 
                                               'i', 'think'])
        self.assertEqual(bigrams, self.bigrams)

    @points_decor(points=10, autograder_name='bigrams')
    def test_calculate_trigrams(self):
        trigrams = text_gen.calculate_trigrams(['i', 'think', 'therefore', 
                                               'i', 'am', 'i', 'think', 
                                               'i', 'think'])
        self.assertEqual(trigrams, self.trigrams)

    def test_bigram_text_correct_length(self):
        text = text_gen.random_bigram_text('i', self.bigrams, 10)
        self.assertEqual(len(text.split()), 10)

    def test_bigram_text_correct_start(self):
        text = text_gen.random_bigram_text('i', self.bigrams, 10)
        self.assertEqual(text.split()[0], 'i')
        text = text_gen.random_bigram_text('think', self.bigrams, 10)
        self.assertEqual(text.split()[0], 'think')

    def test_bigram_text_possible(self):
        words = text_gen.random_bigram_text('i', self.bigrams, 100).split()
        prev = 'i'
        for i in range(1, len(words)):
            current = words[i]
            self.assertGreaterEqual(self.bigrams[prev][current], 0)
            prev = current

    # Trigram Tests ------------

    def test_trigram_text_correct_length(self):
        text = text_gen.random_trigram_text('i', 'think', self.bigrams,
                                            self.trigrams, 10)
        self.assertEqual(len(text.split()), 10)

    def test_trigram_text_correct_start(self):
        text = text_gen.random_trigram_text('i', 'think', self.bigrams,
                                            self.trigrams, 10)
        self.assertEqual(text.split()[0], 'i')
        self.assertEqual(text.split()[1], 'think')
        text = text_gen.random_trigram_text('am', 'i', self.bigrams,
                                            self.trigrams, 10)
        self.assertEqual(text.split()[0], 'am')
        self.assertEqual(text.split()[1], 'i')

    def test_trigram_text_possible(self):
        words = text_gen.random_trigram_text(
            'i', 'think', self.bigrams, self.trigrams, 100).split()
        prev1 = 'i'
        prev2 = 'think'
        for i in range(2, len(words)):
            current = words[i]
            self.assertGreaterEqual(self.trigrams[(prev1, prev2)][current], 0)
            prev1 = prev2
            prev2 = current

def argument_parse():
    parser = argparse.ArgumentParser(description='unittest wrapper')

    parser.add_argument('-normalizePoints', action='store_true',
                        dest='normalize_points', required=False,
                        help='return score between 0 and 100')

    return parser.parse_args()

if __name__ == '__main__':
    parms = argument_parse()

    try:
        unittest.main()
    except:
        print('in except from main')
        pass

    points = points_decor.return_points()
    sys.exit(points)


    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(TestNGrams)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(result)
 
    with open('results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
    """
