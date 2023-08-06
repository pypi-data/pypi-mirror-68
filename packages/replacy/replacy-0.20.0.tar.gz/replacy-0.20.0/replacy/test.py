class TestResources:
    self __init__(self, nlp, match_dict_path):
        



import pytest
import spacy
from replacy import ReplaceMatcher
from replacy.db import load_json

from functional import seq
xfail = pytest.mark.xfail

nlp = spacy.load("en_core_web_sm")

rmatch_dict = load_json("./resources/match_dict.json")
r_matcher = ReplaceMatcher(nlp, rmatch_dict)

def test_rules_positive():
    for rule_name in r_matcher.match_dict:
        print(rule_name)
        rule_suggestions = []
        for suggestion in r_matcher.match_dict[rule_name]["suggestions"]:
            rule_suggestions.append(" ".join([t["TEXT"] for t in suggestion]))

        rule_suggestions = (seq(rule_suggestions)
                            .map(lambda phrase: nlp(phrase))
                            .map(lambda doc: " ".join([token.lemma_ for token in doc]))
                            .list())

        test_set = r_matcher.match_dict[rule_name]["test"]
        positive_set = test_set["positive"]

        for positive_sent in positive_set:
            all_suggestions = (
                seq(r_matcher(positive_sent))
                .flat_map(lambda span: span._.suggestions)
                .map(lambda suggestion: nlp(suggestion))
                .map(lambda doc: " ".join([token.lemma_ for token in doc]))
                .list()
            )

            assert (
                len(set(rule_suggestions).intersection(set(all_suggestions))) > 0
            ), "should correct"


@xfail(raises=AssertionError)
def test_rules_negative():
    for rule_name in r_matcher.match_dict:

        rule_suggestions = []
        for suggestion in r_matcher.match_dict[rule_name]["suggestions"]:
            rule_suggestions.append(" ".join([t["TEXT"] for t in suggestion]))

        rule_suggestions = (seq(rule_suggestions)
                            .map(lambda phrase: nlp(phrase))
                            .map(lambda doc: " ".join([token.lemma_ for token in doc]))
                            .list())

        test_set = r_matcher.match_dict[rule_name]["test"]
        negative_set = test_set["negative"]

        for negative_sent in negative_set:
            all_suggestions = (
                seq(r_matcher(negative_sent))
                .flat_map(lambda span: span._.suggestions)
                .map(lambda suggestion: nlp(suggestion))
                .map(lambda doc: " ".join([token.lemma_ for token in doc]))
                .list()
            )

            assert (
                len(set(rule_suggestions).intersection(set(all_suggestions))) > 0
            ), "should correct"

"""
def test_test_completeness():  # sic
    for rule_name in r_matcher.match_dict:
        test_set = r_matcher.match_dict[rule_name]["test"]
        assert (
            len(test_set["positive"]) > 0 and len(test_set["negative"]) > 0
        ), "missing test data"
"""