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
