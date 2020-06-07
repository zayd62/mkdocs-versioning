import os
import pathlib
import shutil

import yaml
from mkdocs import config as mkconfig
from mkdocs.commands import build


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

    # open config file for writing
    outfile = open('mkdocs.test.yml', 'w')

    # change sitename so that the version number is replaced with the string "Version Page"
    site_name = site_name.replace(version_num, 'Version Page')

    # calculate where the built version page should be stored.
    # i.e. with all the built docs
    head, tail = os.path.split(site_dir)
    built_docs_path = head

    # clean up old files. need to do manually so that built docs are kept but
    # built docs are in folders
    # refactor https://github.com/zayd62/mkdocs-versioning/pull/45#issuecomment-605449689
    item_to_delete = ['assets', 'search']
    with os.scandir(built_docs_path) as files:
        for f in files:
            if not f.is_dir():
                os.remove(f.path)
            elif f.name in item_to_delete:
                shutil.rmtree(f.path)

    # find the built docs and sort them in order and reverse them
    built_docs = sorted(os.listdir(head))
    built_docs.reverse()

    # take list of built docs and create nav item
    nav = []

    # in order to fix issue #48 (https://github.com/zayd62/mkdocs-versioning/issues/48)
    # we rename the original md files to have a "." so it is ignored when version selection page is built

    # add "." to file name
    for root, dirs, files in os.walk(config['docs_dir']):
        for name in files:
            path = pathlib.Path(os.path.join(root, name))
            # add "." to the md file
            filename = path.name
            if path.suffix == '.md':
                path.replace(path.with_name('.' + filename))

    # creating version.md page
    version_page_name = 'index.md'
    path_of_version_md = os.path.join(config['docs_dir'], version_page_name)
    with open(path_of_version_md, 'w') as f:
        f.write('# Welcome to version selector')
        f.write('\n')
        f.write('Use the navigation items to select the version of the docs you want to see.')

    config_path = os.path.realpath(outfile.name)
    homedict = {'Home': version_page_name}
    nav.append(homedict)

    # building paths for each version
    for i in built_docs:
        nav_item = {}
        nav_item[i] = i + '/'
        nav.append(nav_item)

    # remove mkdocs versioning plugin
    for j in inyaml['plugins']:
        if 'mkdocs-versioning' in j:
            inyaml['plugins'].remove(j)

    # if there are no plugins left installed, remove the plugin config otherwise errors will occur
    if len(inyaml['plugins']) <= 0:
        del inyaml['plugins']

    # replace the nav
    inyaml['nav'] = nav

    # replace site_dir
    inyaml['site_dir'] = built_docs_path

    # replace site_name
    inyaml['site_name'] = site_name

    # write config file
    yaml.dump(inyaml, outfile, default_flow_style=False)
    outfile.close()

    cnfg_file = open(config_path, 'rb')
    built_config = mkconfig.load_config(cnfg_file)
    build.build(built_config, dirty=True)
    cnfg_file.close()

    # delete tempdir
    # shutil.rmtree(tempdir)

    # delete outfile
    os.remove(config_path)

    # remove "." from md file
    for root, dirs, files in os.walk(config['docs_dir']):
        for name in files:
            path = pathlib.Path(os.path.join(root, name))
            # remove "." from the md file
            if path.suffix == '.md':
                filename = path.name.strip('.')
                path.replace(path.with_name(filename))
