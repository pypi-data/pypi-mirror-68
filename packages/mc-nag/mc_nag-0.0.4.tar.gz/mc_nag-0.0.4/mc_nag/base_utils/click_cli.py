"""Click CLI Module."""
import click

# pylint: disable=too-many-arguments

COMMON_OPTIONS = [
    click.option('--enable-standard-rules/--disable-standard-rules',
                 default=True,
                 help='Allows for enabling/disabling the standard rule set ' +  # noqa: W504
                 'that ships with mc-nag.'),
    click.option('--custom-platform-rules-dir', '-C', multiple=True,
                 type=click.Path(exists=True), default=None,
                 help='Path to a directory containing custom rules. ' +  # noqa: W504
                 'Allows multiple.')
]
MAIN_OPTIONS = COMMON_OPTIONS + [
    click.option('--rules', is_flag=True),
    click.option('--filepath', '-f', type=click.Path(exists=True),
                 required=False),
    click.option('--output', '-o', default='text',
                 type=click.Choice(['text', 'json', 'yaml', 'none'],
                                   case_sensitive=False)),
    click.option('--paramfile', '-p', type=click.Path(exists=True)),
    click.option('--verbose', '-v', count=True)
]


def add_click_options(options):
    """Decorate with Click options."""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options
