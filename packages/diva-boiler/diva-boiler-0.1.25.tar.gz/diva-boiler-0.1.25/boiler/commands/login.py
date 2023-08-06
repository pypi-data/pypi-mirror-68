import webbrowser

import click
import requests

from boiler import BOILER_CONFIG_FILE, cli, update_config_value


def _is_valid_stumpf_token(stumpf_url: str, token: str) -> bool:
    # note - don't use the boiler session since that could have an old token,
    # and automatically fails on auth failures.
    return requests.get(stumpf_url + '/api/v1/user/me', headers={'X-Stumpf-Token': token}).ok


@click.group(name='login', short_help='authenticate with various services')
@click.pass_obj
def login(ctx):
    pass


@login.command(name='stumpf', help='authenticate with stumpf')
@click.pass_obj
def login_stumpf(ctx):
    click.echo('A browser window has been opened, login and copy the token to login.', err=True)
    webbrowser.open(ctx['stumpf_url'] + '/login?next=/token')

    while True:
        stumpf_token = click.prompt('Token', err=True)
        if _is_valid_stumpf_token(ctx['stumpf_url'], stumpf_token):
            update_config_value(BOILER_CONFIG_FILE, 'stumpf_token', stumpf_token)
            return click.echo(click.style('You are now logged in.', fg='green'), err=True)
        else:
            click.echo(
                click.style(
                    "Your token doesn't appear to be valid, did you copy/paste correctly?",
                    fg='yellow',
                ),
                err=True,
            )


cli.add_command(login)
