import os
import sys
import time
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class Version(BasePlugin):
    config_scheme = (
        ('rebuild', config_options.Type(bool, default=False)),
    )

    def on_config(self, config, **kwargs):

        # extract the version number
        try:
            version = config['extra']['version']
        except KeyError as e:
            print(e)
            print('Warning: ' +
                  'no version detected in mkdocs.yml.You should specify a version number (ideally) according to semantic versioning in mkdocs.yml. exiting')
            sys.exit(1)

        # changing the site name to include the verison number
        config['site_name'] = config['site_name'] + ' - ' + version
        print('the new site_name:  ', config['site_name'])

        # creating new directory from site_dir and version number
        new_dir = os.path.join(config['site_dir'], config['extra']['version'])
        print("the new build directory is", new_dir)

        # check if rebuild is false
        # check if docs for specified version in config already exists
        # if both cases are true, program should exit as docs that already exist should not have to be rebuilt
        if os.path.isdir(new_dir) and self.config['rebuild'] is False:
            print("A documentation with the version", version,
                  "already exists. You should not need to rebuild a version of the documentation that is already built")
            print(
                "if you would like to rebuild, you need to explicitly state that in mkdocs.yml like below: ")
            print("""
            plugins:
              - mkdocs-versioning:
                  rebuild: True
            """)
            print("exiting...")
            sys.exit(1)

        # assign new site_dir to new_dir
        config['site_dir'] = new_dir
