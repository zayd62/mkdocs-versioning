import os
import shutil
import subprocess
import tempfile

import yaml


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
    item_to_delete = ['assets', 'search']
    with os.scandir(built_docs_path) as files:
        for f in files:
            if not f.is_dir() or (f.name in item_to_delete):
                try:
                    os.remove(f.path)
                # PermissionError happens in OSX see:
                # https://github.com/zayd62/mkdocs-versioning/issues/32
                except (IsADirectoryError, PermissionError):
                    shutil.rmtree(f.path)

    # find the built docs and sort them in order and reverse them
    built_docs = sorted(os.listdir(head))
    built_docs.reverse()

    # take list of built docs and create nav item
    nav = []

    # creating tempdir to be docs_dir
    tempdir = tempfile.mkdtemp()

    # set docs_dir to tempdir
    inyaml['docs_dir'] = tempdir


    # test.pypi does not upload version.md so it needs to be manually created
    path_of_version_md = os.path.join(tempdir, 'index.md')
    with open(path_of_version_md, 'w') as f:
        f.write('# Welcome to version selector')
        f.write('\n')
        f.write('Use the navigation items to select the version of the docs you want to see.')


    config_path = os.path.realpath(outfile.name)
    homedict = {'Home': 'index.md'}
    nav.append(homedict)

    # building paths for each version
    version_path_pair = []
    for i in built_docs:
        nav_item = {}
        nav_item[i] = i + '/'
        version_path_pair.append(nav_item)
    versiondict = {'Version Select': version_path_pair}
    nav.append(versiondict)

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

    # run mkdocs build
    subprocess.run(['mkdocs', 'build', '--dirty',
                    '--config-file', config_path])

    # delete tempdir
    shutil.rmtree(tempdir)

    # delete outfile
    os.remove(config_path)
