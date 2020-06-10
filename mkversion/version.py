import os
import pathlib
import shutil

import yaml
from mkdocs import config as mkconfig
from mkdocs.commands import build


def clean_old_files(items_to_delete, built_docs_path, plugin_config):
    with os.scandir(built_docs_path) as files:
        for f in files:
            if not f.is_dir():
                os.remove(f.path)
            elif f.name in items_to_delete or f.name in plugin_config['exclude_from_nav']:
                shutil.rmtree(f.path)


def hide_documentation(config):
    for root, dirs, files in os.walk(config['docs_dir']):
        for name in files:
            path = pathlib.Path(os.path.join(root, name))
            # add "." to the md file
            filename = path.name
            if path.suffix == '.md':
                path.replace(path.with_name('.' + filename))


def unhide_documentation(config):
    for root, dirs, files in os.walk(config['docs_dir']):
        for name in files:
            path = pathlib.Path(os.path.join(root, name))
            # remove "." from the md file
            if path.suffix == '.md':
                filename = path.name.strip('.')
                path.replace(path.with_name(filename))


def build_default_version_page(path_of_version_md):
    with open(path_of_version_md, 'w') as f:
        f.write('# Welcome to version selector')
        f.write('\n')
        f.write('Use the navigation items to select the version of the docs you want to see.')


def version(config, plugin_config):
    """
    Function that handles the versioning

    Args:
        config: the config file as a dictionary
        plugin_config: the plugins config options (version number)

    """
    # extract information from config
    version_num = plugin_config['version']
    site_name = config['site_name']
    site_dir = config['site_dir']
    config_path = config['config_file_path']

    # read mkdocs.yml
    infile = open(config_path, 'r')
    inyaml = yaml.safe_load(infile)
    infile.close()

    # change sitename so that the version number is replaced with the string "Version Page"
    site_name = site_name.replace(version_num, 'Version Page')

    # calculate where the built version page should be stored.
    # i.e. with all the built docs
    built_docs_path, tail = os.path.split(site_dir)

    # clean up old files. need to do manually so that built docs are kept but
    # built docs are in folders
    # refactor https://github.com/zayd62/mkdocs-versioning/pull/45#issuecomment-605449689
    items_to_delete = ['assets', 'search']
    clean_old_files(items_to_delete, built_docs_path, plugin_config)

    # find the built docs and sort them in order and reverse them
    built_docs_list = sorted(os.listdir(built_docs_path))
    built_docs_list.reverse()

    # in order to fix issue #48 (https://github.com/zayd62/mkdocs-versioning/issues/48)
    # rename the original md files to have a "." so it is ignored when version selection page is built
    hide_documentation(config)

    # build default version page
    version_page_name = 'index.md'
    path_of_version_md = os.path.join(config['docs_dir'], version_page_name)
    build_default_version_page(path_of_version_md)

    # take list of built docs and create nav item
    nav = []
    homedict = {'Home': version_page_name}
    nav.append(homedict)

    # building paths for each version
    for i in built_docs_list:
        nav_item = {}
        nav_item[i] = i + '/'
        nav.append(nav_item)

    # remove mkdocs versioning plugin from version config
    for j in inyaml['plugins']:
        if 'mkdocs-versioning' in j:
            inyaml['plugins'].remove(j)

    # if there are no plugins left installed, remove the plugin from version config otherwise errors will occur
    if len(inyaml['plugins']) <= 0:
        del inyaml['plugins']

    # replace the nav
    inyaml['nav'] = nav

    # replace site_dir
    inyaml['site_dir'] = built_docs_path

    # replace site_name
    inyaml['site_name'] = site_name

    # open config file for writing
    with open('mkdocs.version.yml', 'w') as version_config:
        yaml.dump(inyaml, version_config, default_flow_style=False)

    # perform version build
    with open(os.path.realpath(version_config.name), 'rb') as cnfg_file:
        built_config = mkconfig.load_config(cnfg_file)
        build.build(built_config, dirty=True)

    # delete version config
    os.remove(os.path.realpath(version_config.name))

    # unhide original documentation
    unhide_documentation(config)

