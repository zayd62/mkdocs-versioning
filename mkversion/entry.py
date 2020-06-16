import os
import pathlib
import sys
from typing import Dict

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from mkversion.version import hide_md, unhide_md, version


class Entry(BasePlugin):
    config_scheme = (
        ('version', config_options.Type(str)),
        ('exclude_from_nav', config_options.Type(list, default=[])),
        ('version_selection_page', config_options.File())
    )

    def on_config(self, config: Dict[str, str], **kwargs) -> Dict[str, str]:
        """
        An event that alters the config in order to prepare it for versioning as well as perform various checks.

        Args:
            config (Dict[str, str]): the user config (usually mkdocs.yml)

        Returns:
            [Dict[str, str]]: the altered config
        """
        # extract the version number
        version_num = self.extract_version_num()

        # changing the site name to include the version number
        config['site_name'] = config['site_name'] + ' - ' + version_num

        # creating new directory from site_dir and version number
        new_dir = os.path.join(config['site_dir'], version_num)

        # checking if mkdocs is serving or building
        # if serving, DO NOT CHANGE SITE_DIR as an error 404 is returned when visiting built docs
        if not Entry.is_serving(config['site_dir']):
            config['site_dir'] = new_dir

        # check if version selector is in nav
        # if not, then exit
        if not Entry.is_version_selector_in_config(config['nav']):
            sys.exit(2)

        # check if docs for specified version in config already exists
        # if true, program should exit as docs that already exist should not have to be rebuilt
        if os.path.isdir(new_dir):
            print('A documentation with the version', version_num, 'already exists.')
            print('You should not need to rebuild a version of the documentation that is already built')
            print('if you would like to rebuild, you need to delete the folder:', version_num, '. Exiting...')
            sys.exit(1)

        # if a custom version page is defined in the config, then hide it for the initial build
        if self.config['version_selection_page'] is not None:
            version_page_path = os.path.join(config['docs_dir'], self.config['version_selection_page'])
            version_page_path = pathlib.Path(version_page_path)
            if os.path.exists(version_page_path.absolute()):
                hide_md(version_page_path.absolute())
        return config

    def on_post_build(self, config: Dict[str, str], **kwargs) -> Dict[str, str]:
        """
        An event that occur after the documentation has been built. This triggers building the version selection page as well as performing several more check.

        Args:
            config (Dict[str, str]): the user config (usually mkdocs.yml)

        Returns:
            [Dict[str, str]]: the user config
        """
        # if serving, then we do not need to build the version page
        if Entry.is_serving(config['site_dir']):
            print('mkdocs is serving not building so there is no need to build the version page')
        elif self.config['version_selection_page'] is not None:
            # we unhide the custom version selection page
            version_page_path = os.path.join(config['docs_dir'], self.config['version_selection_page'])
            version_page_path = pathlib.Path(version_page_path)

            # build path of HIDDEN custom version selection page and unhide
            # after building the docs
            version_page_path_with_dot = version_page_path.with_name('.' + version_page_path.name)
            if os.path.exists(version_page_path_with_dot.absolute()):
                unhide_md(version_page_path_with_dot.absolute())

        # build version page
        version(config, self.config)
        return config

    def extract_version_num(self) -> str:
        """
        extracts the version "number"

        Returns:
            str: returns the version number as a string
        """
        try:
            version_num = self.config['version']
            return version_num
        except KeyError as e:
            print(e)
            print('Warning: ' +
                  'no version detected in mkdocs.yml.You should specify a version number (ideally) according to '
                  'semantic versioning in mkdocs.yml. exiting')
            sys.exit(1)

    @staticmethod
    def is_serving(site_path: str) -> bool:
        """
        detects if mkdocs is serving or building by looking at the site_dir in config. if site_dir is a temp
        directory, it assumes mkdocs is serving

        Arguments:
            site_path {str} -- the site_dir path

        Returns:
            bool -- true if serving, false otherwise
        """

        # if mkdocs is serving, the string "tmp" will be in the path
        # str.find('tmp') will return -1 if "tmp" is NOT FOUND
        if site_path.find('tmp') == -1:
            return False
        else:
            return True

    @staticmethod
    def is_version_selector_in_config(nav: Dict[str, str]) -> bool:
        """
        Check to see if the version selector is in the users config and with the appropriate value (usually, mkdocs.yml)

        Args:
            nav (Dict[str, str]): a dictionary of the user config

        Returns:
            bool: True if config contains version selector, false otherwise
        """
        for i in nav:
            if 'version selector' in [j.lower() for j in i.keys()]:
                # if true, check if the value is '../'
                for k in i.values():
                    if k == '../':
                        return True
                    else:
                        print('Version Selector not specified correctly')
                        return False
