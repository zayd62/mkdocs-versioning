# Getting Started

## Installing mkdocs-versioning

The install is very similar to a standard mkdocs project. The first step is to install mkdocs as well as mkdocs-versioning
using pip:

```
pip install mkdocs
pip install mkdocs-versioning
```

Next step is to initialise a new mkdocs project. In the root of your project:

```
mkdocs new .
```

This should generate a `mkdocs.yml` file as well as a folder called `docs`

## Setting up `mkdocs.yml`

Your `mkdocs.yml` file will be slightly different than normal. The key differences are

1. The need to register the mkdocs-versioning plugin
2. Add the version number as a config option for the plugin. Recommend following [Semantic Versioning](https://semver.org)
3. Change the [edit_uri](https://www.mkdocs.org/user-guide/configuration/#edit_uri). This is because that the edit uri
will point to the latest version of the source file mentioned in `mkdocs.yml` not the version of the page specific to 
the version of the doc you are in. 

    For example, if you were in version `1.0.0` of a page and the next version of your doc is version `1.1.0`.
    Using the automatically generated edit uri will take you to the version `1.1.0` of the doc not version `1.0.0`
    
4. Adding ```Version: ‘../’``` to the nav

A sample config is available below to simply copy-paste into ```mkdocs.yml```:

```
site_name: mkdocs-versioning
repo_url: <URL GOES HERE>
repo_name: <USERNAME/REPOSITORY_NAME>
edit_uri: ''
plugins:
  - mkdocs-versioning:
      version: <VERSION NUMBER GOES HERE>
nav:
  - Home : 'index.md'
  - Nav item: 'file_name.md'
  - Version: '../'
``` 

!!! important
    the ```Version: '../'``` nav item is crucial. failure to add it to the nav means that there is no easy way to 
    navigate to the version selection page apart from manually navigating to the URL (which is as simple as removing 
    the version number)

You then write the docs [as normal](https://www.mkdocs.org/user-guide/writing-your-docs/) and when you have finished, 
simply run the build command ```mkdocs build```. You can preview the docs using ```mkdocs serve```

!!! note
    While serving, the version page will NOT be built. to view the version page, you will need to build the docs. You 
    can then serve the built docs using built in python http server
    
    ```python
    # for python 2
    python -m SimpleHTTPServer
    
    # for python 3
    python3 -m http.server
    ```

## Common Errors

### Rebuilding previously built docs

If you are trying to rebuild a version of the docs that has already been built, mkdocs will NOT overwrite it. This is 
because you should not have to be rebuilding a previous version of the doc; rather, all changes should be reflected
in a new version of the software and ideally, should be following [Semantic Versioning](https://semver.org). However, 
should you need to rebuild previous versions of your documentation (for example, spelling mistakes or missing documentation),
simply deleting the directory will do (if you need to rebuild version `1.3.0`, delete the folder labeled `1.3.0`).  

### Correct version numbers not showing in the version selection page

The version selection page depends on the built docs found in the `site` directory, specifically the names of the folders.
This could result in missing/incorrect documentation versions in the version selection page. One reason for this is that
the built docs are generally stored somewhere else (e.g. `gh-pages` branch) and source file (both code and .md files) are 
stored in the master branch. This means that you mau not have the built docs which are required for 
building the versions page correctly. 

One way to mitigate this is by using the [sync](../CLI commands#sync) command which will sync the `gh-pages` branch to 
your local machine. Run this before you work on your next documentation will ensure that all the docs you have previously
built will be synced to your local machine so that when you run `mkdocs build`, the versions page will be built correctly

#### What if documentation is not stored in `gh-pages` branch

You will then need to manually sync **FROM** where the docs are built **TO** the directory where built docs are saved (usually the
`site` directory).