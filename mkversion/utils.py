import argparse
from pprint import pprint

from mkdocs.commands import gh_deploy
from mkdocs import config, exceptions


def deploy(args: argparse.Namespace):
    """
    Deploy to Github Pages

    Args:
        args (argparse.Namespace): A Namespace object contaning all the command line arguments

    Raises:
        exceptions.ConfigurationError
    """
    print('vars(args) -->', vars(args))

    try:
        cfg = config.load_config(config_file=args.config_file, remote_branch=args.remote_branch, remote_name=args.remote_name)
        gh_deploy.gh_deploy(cfg, message=args.message, force=args.force, ignore_version=args.ignore_version)

    except exceptions.ConfigurationError as e:
        raise SystemExit('\n' + str(e))

