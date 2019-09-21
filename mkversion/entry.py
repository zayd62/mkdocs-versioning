import os
import sys
from .version import Version
from mkdocs import utils
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class Entry(BasePlugin):
    config_scheme = (
        ('version', config_options.Type(utils.string_types)),
    )

    def on_config(self, config, **kwargs):
        # extract the version number
        try:
            version_num = self.config['version']
        except KeyError as e:
            print(e)
            print('Warning: ' +
                  'no version detected in mkdocs.yml.You should specify a version number (ideally) according to semantic versioning in mkdocs.yml. exiting')
            sys.exit(1)

        # changing the site name to include the verison number
        config['site_name'] = config['site_name'] + ' - ' + version_num

        # creating new directory from site_dir and version number
        new_dir = os.path.join(config['site_dir'], version_num)

        # checking if mkdocs is serving or building
        # if serving, DO NOT CHANGE SITE_DIR as an error 404 is returned when visting built docs
        if not is_serving(config['site_dir']):
            config['site_dir'] = new_dir

        # check if rebuild is false
        # check if docs for specified version in config already exists
        # if both cases are true, program should exit as docs that already exist should not have to be rebuilt
        if os.path.isdir(new_dir):
            print("A documentation with the version", version_num,
                  "already exists. You should not need to rebuild a version of the documentation that is already built")
            print(
                "if you would like to rebuild, you need to delete the folder:", version_num, ". Exiting...")
            sys.exit(1)
        return config

    def on_post_build(self, config, **kwargs):
        if is_serving(config['site_dir']):
            print('mkdocs is serving not building so there is no need to build the version page')
        else:
            Version(config, self.config)
        return config


def is_serving(site_path: str) -> bool:
    """
    detects if mkdocs is serving or building by looking at the site_dir in config. if site_dir is a temp
    dierectory, it assumes mkdocs is serving

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
