import pytest
from sentenceverifier.verifysentence import *


class TestsSentenceVerifier:

    @pytest.mark.parametrize("sentence,positivity,expected", [
        ("The book was good.", 1, 1),
        ("James is smart, handsome, and funny.", 1, 1),
        ("Ronaldo Madrit", 1, 0),
        ("Einstein physicist", -1, 0),
        ("The book was good.", -1, -1),
        ("James is smart, handsome, and funny.", -1, -1),
        ("The book was not good and the plot was not interesting.", 1, -1),
        ("James is not smart, handsome, and funny.", 1, -1)
    ])
    def test_source_sentence_verify(self, sentence, positivity, expected):
        assert source_sentence_verify(sentence, positivity) == expected

    @pytest.mark.parametrize("string,sentence,expected", [
        ("The book was good", "was good", 1),
        ("James is smart, handsome, and funny.", "James is playing football", 0),
        ("Near the beginning of his career", "Near the beginning of his career", 1),
        ("and with his subsequent theory of gravitation in", "with theory in", 1),
        ("and with his subsequent theory of gravitation in", "theory of big bum", 0)
    ])
    def test_in_string(self, sentence, string, expected):
        assert in_string(sentence, string) == expected

    @pytest.mark.parametrize("sentence, page_sentences, positivity, expected", [
        ("James is an actor", ["James is an actor", "James plays in cos", "James is not a good actor"], 1, 0),
        ("James is an actor", ["James is an actor and a good singer", "James plays in cos", "James is high"], 1, 1),
        ("James is an footballer", ["James is an actor", "James plays in cos", "James is high"], 1, 0),
        ("James is an actor", ["James is an actor and a good singer", "James is an actor and a good singer",
                               "James is an actor and a good singer"], 1, 3),
        ("James is an actor", ["James is an actor and a good singer", "James is an actor and a good singer",
                               "James is an actor and a good singer"], -1, -3),
        ("James is an actor", ["James is an actor and a good singer", "James plays in cos", "James is high"], -1, -1)
    ])
    def test_verify_source(self, sentence, page_sentences, positivity, expected):
        assert verify_source(sentence, page_sentences, positivity) == expected

    @pytest.mark.parametrize("sentence, precision, positivity, expected", [
        ("Ronaldo won Champions League", 5, 1, 1),
        ("Ronaldo won Champions League", 5, -1, -1),
        ("Thriller is the best-selling album", 5, 1, 1),
        ("Thriller is the best-selling album", 5, -1, -1),
        ("Poland is in Europe", 5, -1, -1)
    ])
    def test_verify_input(self, sentence, precision, positivity, expected):
        assert verify_input(sentence, precision, positivity) == expected
