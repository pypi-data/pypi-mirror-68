"""Utility functions related to rule evaluation."""

import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from itertools import chain
from .printers import BCOLORS


class RuleEvaluator:
    """Engine to evaluate rules.

    This class will find all rules inside the supplied standard rules
    directory and evaluate them against the given template model.
    :param model: Template data model built from a template.
    """

    def __init__(self, model, standard_rules_dir, enable_standard_rules=True,
                 custom_rules_dirs=None):
        """Assign arguments as attributes and prepare rules."""
        self.model = model
        self._standard_rules_dir = standard_rules_dir
        self.rule_set = self._retrieve_rule_objects(enable_standard_rules,
                                                    custom_rules_dirs)

    def evaluate_rules(self):
        """Evaluate given rules against the data model."""
        violations_by_rule = {}
        severity_counts = {}

        for rule in self.rule_set:
            # Instantiate rule
            rule_object = rule(self.model)

            # Evaluate rule
            violating_resources = rule_object.evaluate()

            # Continue to next rule if no violations found
            if not violating_resources:
                continue

            # Add to violations by rule
            if rule not in violations_by_rule:
                violations_by_rule[rule] = []
            violations_by_rule[rule] += violating_resources

            # Add to severity counter
            if rule_object.severity not in severity_counts:
                severity_counts[rule_object.severity] = 0
            severity_counts[rule_object.severity] += 1

        return violations_by_rule, severity_counts, self.rule_set

    def display_rules(self):
        """Output list of rules and rule IDs in given format.

        :param output: Format in which the output should be.
        :param verbose: Level of verbosity.
        """
        # Dict to hold values for duplicate checking
        dupe_rules = {}
        rev_dict = {}

        # Gather table formatting information & print header
        left_pad = max(max([len(rule.rule_id) for rule in self.rule_set]), 7)
        right_pad = max(max([len(rule.__name__) for rule in self.rule_set]), 9)
        print(f'{"Rule ID":{left_pad}} | Rule Name')
        print(f"{''.rjust(left_pad, '-')} | {''.rjust(right_pad, '-')}")

        # Iterate over all found rules and build rev dict
        for rule in sorted(self.rule_set, key=lambda x: x.rule_id):
            print(f'{rule.rule_id:{left_pad}} | {rule.__name__}')
            rev_dict.setdefault(rule.rule_id, set()).add(
                f'{rule.__name__} ({rule.__module__}.py)'
            )

        # Find duplicate rule IDs
        for key, values in rev_dict.items():
            if len(values) > 1:
                dupe_rules[key] = values

        # Output
        if dupe_rules:
            left_pad = max(max([len(key) for key in dupe_rules]), 17)
            print(f'\n{BCOLORS["ERROR"]}Found duplicate rule IDs!' +  # noqa: W504
                  f'{BCOLORS["ENDC"]}\n')
            print(f'{"Duplicate Rule ID":{left_pad}} | Duplicate Rule Names')
            for key, values in dupe_rules.items():
                print(f"{''.rjust(left_pad, '-')} | {''.rjust(20, '-')}")
                print(f"{key:{left_pad}} | " +  # noqa: W504
                      f',\n{"".rjust(left_pad)} | '.join(values))
        else:
            print(f'\n{BCOLORS["OKGREEN"]}No duplicates{BCOLORS["ENDC"]} 🎉')

        return dupe_rules

    def _retrieve_rule_objects(self, enable_standard_rules=True,
                               custom_rules_dirs=None):
        """Return list of rule classes to evaluate.

        Based on this StackOverflow info:
        https://stackoverflow.com/a/41904558
        """
        paths = []

        # Platform-specific standard rules path
        if enable_standard_rules:
            paths.append(self._standard_rules_dir)

        # Add custom rules directories to paths if existent
        if custom_rules_dirs:
            paths += custom_rules_dirs

        # Set to hold found rules
        rules = set()
        found_rule_modules = set()

        # Iterate over all rules paths (standard and custom)
        for path, _, files in chain.from_iterable(os.walk(path)
                                                  for path in paths):
            # Iterate over .py files in path
            for py_file in [f[:-3] for f in files
                            if f.endswith('.py') and f != '__init__.py']:
                # Prepare module path to import
                module_path = f'{path}/{py_file}.py'

                # Import .py file as a module
                spec = spec_from_file_location(py_file, module_path)
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)

                # Retrieve list of classes from module
                classes = [getattr(mod, x) for x in dir(mod)
                           if isinstance(getattr(mod, x), type)
                           and x != 'BaseRule']  # noqa: W503

                # Set new found class names as part of the system modules
                for cls in classes:
                    setattr(sys.modules[__name__], cls.__name__, cls)

                # Add new found classes to rules set
                if py_file not in found_rule_modules:
                    rules.update(classes)
                    found_rule_modules.add(py_file)

        return rules
