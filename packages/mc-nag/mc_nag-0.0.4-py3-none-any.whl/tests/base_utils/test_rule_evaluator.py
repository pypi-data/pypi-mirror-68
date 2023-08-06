"""Tests for rule evaluation logic."""

import re
from pytest import fixture, raises
from mc_nag.base_utils import read_template_file
from mc_nag.base_utils.models.rule import (
    BaseRule,
    ERROR as RULE_ERROR,
    WARNING as RULE_WARNING
)
from mc_nag.base_utils.rule_evaluator import RuleEvaluator
from tests.rules.standard.standard_rule import StandardRule
from tests.rules.custom.custom_rule_for_option_testing import \
    CustomPlatformRule
from tests.fixtures import TestTemplate

# pylint: disable=redefined-outer-name

TEMPLATES_PATH = 'tests/templates'
VALID_TEMPLATE = f'{TEMPLATES_PATH}/parser_test_good.json'
INVALID_TEMPLATE = f'{TEMPLATES_PATH}/parser_test_bad.json'


@fixture(scope='module')
def valid_template_model():
    """Return template model for a valid template."""
    return TestTemplate(read_template_file(VALID_TEMPLATE))


@fixture(scope='module')
def invalid_template_model():
    """Return template model for an invalid template."""
    return TestTemplate(read_template_file(INVALID_TEMPLATE))


def test_rule_evaluator_standard_rules():
    """Happy Path: Ensure we can import standard rules."""
    rule_evaluator = RuleEvaluator(None, 'tests/rules/standard')

    assert StandardRule.__name__ in \
        [rule.__name__ for rule in rule_evaluator.rule_set]


def test_rule_evaluator_custom_rules():
    """Happy Path: Ensure we can import custom rules."""
    rule_evaluator = RuleEvaluator(None, 'tests/rules/standard', True,
                                   ['tests/rules/custom'])

    rule_names = [rule.__name__ for rule in rule_evaluator.rule_set]
    assert StandardRule.__name__ in rule_names
    assert CustomPlatformRule.__name__ in rule_names


def test_rule_evaluator_only_custom_rules():
    """Happy Path: Ensure we can import only custom rules."""
    rule_evaluator = RuleEvaluator(None, '', False,
                                   ['tests/rules/custom'])

    rule_names = [rule.__name__ for rule in rule_evaluator.rule_set]
    assert StandardRule.__name__ not in rule_names
    assert CustomPlatformRule.__name__ in rule_names


def test_rule_evaluator_no_rules():
    """Sad Path: Ensure we can handle the case when no rules are supplied.

    This should never happen, as it is handled by Click in main.py,
    but good to validate we will get an empty rule_set.
    """
    rule_evaluator = RuleEvaluator(None, None, False)

    assert not rule_evaluator.rule_set


def test_rule_evaluator_passing_template(valid_template_model):
    """Happy Path: Ensure we can evaluate a rule against a valid template."""
    rule_evaluator = RuleEvaluator(valid_template_model,
                                   'tests/rules/standard')
    rule_evaluator.rule_set = set([StandardRule])
    violations_by_rule, violation_counts, rules = rule_evaluator.evaluate_rules()

    assert not violations_by_rule
    assert not violation_counts
    assert rules == {StandardRule}


def test_rule_evaluator_failing_rule(invalid_template_model):
    """Sad Path: Ensure we can evaluate a rule which returns violations."""
    rule_evaluator = RuleEvaluator(invalid_template_model,
                                   'tests/rules/custom')
    rule_evaluator.rule_set = set([CustomPlatformRule])
    violations_by_rule, violation_counts, rules = rule_evaluator.evaluate_rules()

    assert CustomPlatformRule in violations_by_rule
    assert len(violations_by_rule[CustomPlatformRule]) == 1
    assert RULE_WARNING in violation_counts
    assert violation_counts[RULE_WARNING] == 1
    assert rules == {CustomPlatformRule}


def test_rule_evaluator_bad_rule(invalid_template_model):
    """Sad Path: Ensure we raise an exception for a bad rule class."""
    class BadRule(BaseRule):  # pylint: disable=abstract-method
        """Bad rule for testing."""

        rule_id = 'BAD'
        description = 'Bad rule.'
        severity = RULE_ERROR
        category_tags = {"custom-resource"}
        source_tags = {"stelligent"}

    rule_evaluator = RuleEvaluator(invalid_template_model,
                                   'tests/rules/standard')
    rule_evaluator.rule_set = set([BadRule])

    with raises(NotImplementedError, match="'BadRule' must define"):
        _, _, _ = rule_evaluator.evaluate_rules()


def test_rule_evaluator_display_rules_no_dupes(capsys):
    """Happy Path: Display rules without duplicates."""
    RuleEvaluator(None, 'tests/rules/standard').display_rules()

    captured = capsys.readouterr()
    assert re.search('No duplicates', captured.out)
    assert re.search(r'standard-rule.*StandardRule', captured.out)


def test_rule_evaluator_display_rules_with_dupes(capsys):
    """Happy Path: Display rules with duplicates."""
    RuleEvaluator(None, 'tests/rules/standard', True,
                  ['tests/rules/custom']).display_rules()

    captured = capsys.readouterr()
    assert re.search('Found duplicate rule IDs!', captured.out)
    assert re.search(r'Duplicate Rule ID.*Duplicate Rule Names', captured.out)
    assert re.search(
        r'DuplicateCustomPlatformRule \(duplicate_custom_rule_for_testing.py',
        captured.out
    )
