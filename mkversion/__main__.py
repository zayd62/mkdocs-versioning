import argparse
import logging
import os
import sys
from mkdocs import exceptions
from mkversion import deploy


class MyFormatter(logging.Formatter):
    """
    A custom formatter that allows you to specify custom formatting options for the different
    logging levels. If no custom format is specified, it will use the 'base format'

    based on https://stackoverflow.com/a/14859558
    """
    # the base format, used when a format for a specific level is not defined
    base_format = '%(levelname)s: %(asctime)-8s [%(filename)s:%(lineno)d]: %(message)s \n'
    critical_format = base_format

    def __init__(self):
        """
        Sets the base format according to the class variable 'base_format'
        """
        super().__init__(fmt=MyFormatter.base_format, datefmt=None, style='%')

    def format(self, record):
        """
        sets the appropriate format for each level
        See https://docs.python.org/3/library/logging.html#logging.Formatter.format
        """

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.CRITICAL:
            self._style._fmt = MyFormatter.critical_format

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


def main():
    # help definitions

    config_help = "Provide a specific MkDocs config"
    commit_message_help = ("A commit message to use when committing to the Github Pages remote branch. Commit {sha} and MkDocs {version} are available as expansions")
    remote_branch_help = ("The remote branch to commit to for Github Pages. This overrides the value specified in config")
    remote_name_help = ("The remote name to commit to for Github Pages. This overrides the value specified in config")
    force_help = "Force the push to the repository."
    ignore_version_help = "Ignore check that build is not being deployed with an older version of MkDocs."
    #####################################################################
    #            Code for parsing command line arguments                #
    #####################################################################

    # https://docs.python.org/3.7/howto/argparse.html
    # https://docs.python.org/3/library/argparse.html

    # create the arguent parser
    parser = argparse.ArgumentParser(description='A tool that allows the versioning of documentation built using mkdocs')

    # mutually exclusive means that only one option can be supplied. supplying both will result in an error
    group = parser.add_mutually_exclusive_group()

    # "store_true" means that if the argument is provided, the value of the argument is true
    group.add_argument('-v', '--verbose', action='store_true', help='Give more output')
    group.add_argument('-q', '--quiet', action='store_true', help='Give no output')

    # create sub parser
    subparser = parser.add_subparsers(title='Sub-commands', description='List of available sub-commands', help='List of sub-commands')

    # add command deploy
    parser_deploy = subparser.add_parser(
        'deploy', description='Command used to deploy documentation to GitHub Pages', help='Deploy documentation to Github Pages')

    # add argument for deploy command
    parser_deploy.add_argument('-f', '--config-file', help=config_help, metavar='FILE', type=argparse.FileType(mode='rb'))
    parser_deploy.add_argument('-m', '--message', help=commit_message_help)
    parser_deploy.add_argument('-b', '--remote-branch', help=remote_branch_help)
    parser_deploy.add_argument('-r', '--remote-name', help=remote_name_help)
    parser_deploy.add_argument('--force', action='store_true', help=force_help)
    parser_deploy.add_argument('--ignore-version', action='store_true', help=ignore_version_help)

    # writing the arguments to a variable to be accesed
    args = parser.parse_args()

    # if verbose flag not passed on as an argument, this will disable all logging levels
    if not args.verbose:
        logging.disable(logging.CRITICAL)  # This will disable all logging

    # if quiet flag is enabled, stdout (console output) is written to devnull where data is discarded
    if args.quiet:
        sys.stdout = open(os.devnull, 'a')

    #########################################
    #           Code for logging            #
    #########################################

    # create a formatter
    fmt = MyFormatter()

    # code for logging to console
    hdlr_console = logging.StreamHandler(sys.stdout)
    hdlr_console.setFormatter(fmt)
    logging.root.addHandler(hdlr_console)

    '''
    # Code for logging to file
    hdlr_file = logging.FileHandler('spam.log')
    hdlr_file.setFormatter(fmt)
    logging.root.addHandler(hdlr_file)
    '''

    logging.root.setLevel(logging.DEBUG)

    # application code go below here

    # # prints all the arguments
    # print("args", args)

    # print('this is the start of the program. This should appear even if verbosity is disabled, unless the quiet option is enabled')
    # # below are logging levels with "debug" being the lowest and "critical" being the highest
    # logging.debug(
    #     'The lowest level. Used for small details. Usually you care about these messages only when diagnosing problems.')
    # logging.info('Used to record information on general events in your program or confirm that things are working at their point in the program.')
    # logging.warning('Used to indicate a potential problem that doesn’t prevent the program from working but might do so in the future.')
    # logging.error(
    #     'Used to record an error that caused the program to fail to do something')
    # logging.critical(
    #     'The highest level. Used to indicate a fatal error that has caused or is about to cause the program to stop running entirely.')


if __name__ == "__main__":
    main()
