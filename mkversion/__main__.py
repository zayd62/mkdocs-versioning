import argparse
import logging
import os
import sys

from mkversion import utils


def main():
    logging.root.setLevel(logging.DEBUG)
    args = parse_cmd(sys.argv[1:])

    # if verbose flag not passed on as an argument, this will disable all logging levels
    if not args.verbose:
        logging.disable(logging.CRITICAL)  # This will disable all logging

    # if quiet flag is enabled, stdout (console output) is written to devnull where data is discarded
    if args.quiet:
        sys.stdout = open(os.devnull, 'a')

    #########################################
    #        Application code below         #
    #########################################

    if 'func' in vars(args):
        args.func(args)

    # print('this is the start of the program. This should appear even if verbosity is disabled, unless the quiet
    # option is enabled') # below are logging levels with "debug" being the lowest and "critical" being the highest
    # logging.debug( 'The lowest level. Used for small details. Usually you care about these messages only when
    # diagnosing problems.') logging.info('Used to record information on general events in your program or confirm
    # that things are working at their point in the program.') logging.warning('Used to indicate a potential problem
    # that does not prevent the program from working but might do so in the future.') logging.error( 'Used to record
    # an error that caused the program to fail to do something') logging.critical( 'The highest level. Used to
    # indicate a fatal error that has caused or is about to cause the program to stop running entirely.')


def parse_cmd(cmd):

    # help definitions
    config_help = 'Provide a specific MkDocs config'
    commit_message_help = ('A commit message to use when committing to the Github Pages remote branch. Commit {sha} '
                           'and MkDocs {version} are available as expansions')
    remote_branch_help = ('The remote branch to commit to for Github Pages. This overrides the value specified in '
                          'config')
    remote_name_help = 'The remote name to commit to for Github Pages. This overrides the value specified in config'
    force_help = 'Force the push to the repository.'
    ignore_version_help = 'Ignore check that build is not being deployed with an older version of MkDocs.'
    sync_description = 'Used to sync GitHub pages branch to built docs directory. Run if local docs are not the same ' \
                       'as the ones available on Github pages. e.g after cloning the repository '

    #####################################################################
    #            Code for parsing command line arguments                #
    #####################################################################
    # https://docs.python.org/3.7/howto/argparse.html
    # https://docs.python.org/3/library/argparse.html

    # create the argument parser
    parser = argparse.ArgumentParser(
        description='A tool that allows the versioning of documentation built using mkdocs')

    # mutually exclusive means that only one option can be supplied. supplying both will result in an error
    group = parser.add_mutually_exclusive_group()

    # "store_true" means that if the argument is provided, the value of the argument is true
    group.add_argument('-v', '--verbose', action='store_true', help='Give more output')
    group.add_argument('-q', '--quiet', action='store_true', help='Give no output')

    # create sub parser
    subparser = parser.add_subparsers(title='Sub-commands', description='List of available sub-commands',
                                      help='List of sub-commands', dest='subparser_name')

    # add command deploy
    parser_deploy = subparser.add_parser(
        'deploy', description='Command used to deploy documentation to GitHub Pages',
        help='Deploy documentation to Github Pages')
    parser_deploy.set_defaults(func=utils.deploy)  # add default function for deploy command

    # add arguments for deploy command
    parser_deploy.add_argument('-f', '--config-file', help=config_help, metavar='FILE',
                               type=argparse.FileType(mode='rb'))
    parser_deploy.add_argument('-m', '--message', help=commit_message_help)
    parser_deploy.add_argument('-b', '--remote-branch', help=remote_branch_help)
    parser_deploy.add_argument('-r', '--remote-name', help=remote_name_help)
    parser_deploy.add_argument('--force', action='store_true', help=force_help)
    parser_deploy.add_argument('--ignore-version', action='store_true', help=ignore_version_help)

    # add command sync
    parser_sync = subparser.add_parser('sync', description=sync_description, help='Sync GitHub Pages to local docs')
    parser_sync.set_defaults(func=utils.sync)
    parser_sync.add_argument('-f', '--config-file', help=config_help, metavar='FILE', type=argparse.FileType(mode='rb'))

    # add command unhide documentation
    parser_unhide = subparser.add_parser('unhide', description='Unhide the documentation by removing the dot at the beginning of the filename', help='Unhide the documentation')
    parser_unhide.set_defaults(func=utils.unhide_docs)
    parser_unhide.add_argument('path', help='the path to the docs directory', metavar='PATH')

    # check if no arguments were passed. if true, print help
    if len(cmd) == 0:
        parser.print_help()
        sys.exit(1)

    # writing the arguments to a variable to be accessed
    args = parser.parse_args(cmd)
    return args


if __name__ == '__main__':
    main()
