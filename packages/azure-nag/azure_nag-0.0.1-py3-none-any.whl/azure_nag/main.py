"""Main module for executing mc-nag."""

import os
import sys
import click
from mc_nag.base_utils import read_template_file
from mc_nag.base_utils.printers import OutputPrinter
from mc_nag.base_utils.rule_evaluator import RuleEvaluator
from mc_nag.base_utils.click_cli import (
    add_click_options,
    MAIN_OPTIONS
)
from azure_nag.models.azure_template import AzureTemplate

# pylint: disable=too-many-arguments

STANDARD_RULES_DIR = os.path.realpath(
    f'{os.path.dirname(os.path.abspath(__file__))}/rules'
)


@click.pass_context
def list_rules(ctx):
    """Output information about existing rules."""
    rule_evaluator = RuleEvaluator(None, STANDARD_RULES_DIR,
                                   enable_standard_rules=ctx.params.get('enable_standard_rules',
                                                                        True),
                                   custom_rules_dirs=ctx.params.get('custom_platform_rules_dir',
                                                                    None))
    ctx.exit(1 if rule_evaluator.display_rules() else 0)


@click.command()
@add_click_options(MAIN_OPTIONS)
def main(rules=False, filepath=None, output='text', paramfile=None,
         custom_platform_rules_dir=None, enable_standard_rules=True,
         verbose=0):
    """Perform template parsing and rule evaluation."""
    # Validate either --enable-standard-rules is set or a custom platform
    # rules dir is given
    if not (enable_standard_rules or custom_platform_rules_dir):
        raise click.BadParameter(
            "Either '--enable-standard-rules' must be True or " +  # noqa: W504
            "'--custom-platform-rules-dir' must have a value."
        )
    if rules:
        list_rules()  # pylint: disable=no-value-for-parameter

    # Read raw template into string
    if not filepath:
        raise click.BadParameter(
            "--filepath must be a supplied to evaluate rules."
        )
    template_string = read_template_file(filepath)

    # Read raw param file into string, if exists
    parameters_string = None
    if paramfile is not None:
        parameters_string = read_template_file(paramfile)

    # Generate template model
    template_model = AzureTemplate(template_string, parameters_string)

    # Print contents of template_model
    if verbose > 0:
        print(template_model)

    # Instantiate RuleEvaluator and evaluate rules
    rule_evaluator = RuleEvaluator(template_model, STANDARD_RULES_DIR,
                                   enable_standard_rules,
                                   custom_platform_rules_dir)
    violations_dict, violations_counts = rule_evaluator.evaluate_rules()

    # Print violations in plain text
    getattr(OutputPrinter, output)(violations_dict, violations_counts)

    # Exit with either number of ERRORs or 0
    sys.exit(int(violations_counts.get('ERROR', 0)))


if __name__ == "__main__":
    # execute only if run as a script
    main()  # pylint: disable=E1120
