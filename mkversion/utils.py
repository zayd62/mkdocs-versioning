import os
import shutil
import subprocess
import tempfile

from mkdocs import config, exceptions
from mkdocs.commands import gh_deploy
from mkversion.version import unhide_documentation


def deploy(args):
    """
    Deploy to Github Pages

    Args:
        args (argparse.Namespace): A Namespace object contaning all the command line arguments

    Raises:
        exceptions.ConfigurationError
    """

    try:
        cfg = config.load_config(config_file=args.config_file, remote_branch=args.remote_branch, remote_name=args.remote_name)
        gh_deploy.gh_deploy(cfg, message=args.message, force=args.force, ignore_version=args.ignore_version)

    except exceptions.ConfigurationError as e:
        raise SystemExit('\n' + str(e))


def sync(args):
    """
    Pulls the previously built pages from github pages

    Args:
        args (argparse.Namespace): A Namespace object contaning all the command line arguments

    Raises:
        exceptions.ConfigurationError
    """

    cfg = config.load_config(config_file=args.config_file)
    with tempfile.TemporaryDirectory() as tempdir:
        # clone gh-pages branch into a temp dir
        os.chdir(tempdir)
        subprocess.run(['git', 'clone', '-b', cfg['remote_branch'], cfg['repo_url']])
        # noinspection PyArgumentList
        os.chdir(os.listdir()[0])

        # remove old site folder
        try:
            shutil.rmtree(cfg['site_dir'])
            os.mkdir(cfg['site_dir'])  # rmtree deletes folder so you need to recreate folder
        except FileNotFoundError as identifier:
            print(identifier)
            print('no site directory')

        # copy files into site directory
        with os.scandir(os.getcwd()) as files:
            for i in files:
                print(i.name, i.path)
                shutil.move(i.path, cfg['site_dir'])


def unhide_docs(args):
    """
    Unhide documentation

    Args:
        args (argparse.Namespace): A Namespace object contaning all the command line arguments
    """
    docs_path = {'docs_dir': args.path}
    unhide_documentation(docs_path)
