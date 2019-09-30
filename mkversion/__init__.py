name = 'mkdocs-versioning'
import logging
import sys


class MyFormatter(logging.Formatter):
    """
    A custom formatter that allows you to specify custom formatting options for the different
    logging levels. If no custom format is specified, it will use the 'base format'
    based on https://stackoverflow.com/a/14859558
    """
    # the base format, used when a format for a specific level is not defined
    base_format = '%(levelname)s: %(asctime)-8s [%(filename)s:%(lineno)d]: %(message)s \n'

    # defining the critical format
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

