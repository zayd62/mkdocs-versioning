# Home

Welcome to mkdocs-versioning!

mkdocs-versioning is a tool that allows you to version documentation built using [mkdocs](https://github.com/mkdocs/mkdocs/) allowing users to access historical versions of documentation. mkdocs-versioning works by building each documentation version into its own folder and having a central, continuously updating *`version selection page`* which points to each version built. 

## Design

mkdocs-versioning is designed with the following principles in mind:

1. **Theme agnostic**: The plugin should work with any mkdocs theme. mkdocs-versioning takes advantage of the navigation links to implement versioning. 
2. **Strict versioning**: Once a documentation is built, it should **NOT** be overwritten. mkdocs-versioning uses a centralised, continuously updated version selection page which then, using the navigation links, point to built docs. The built docs then have a **relative link** which then points to the version selection page.
3. **Stateless**: Stateless means that no extra information is stored anywhere in order for the plugin to work. All the plugin needs is the previously built docs, a **new** version number and it can build the new docs, the version selection page and have the previous verions of the built docs available and accessible.


## Install

It is **highly** recommended that you use Python [Virtual Environments](https://docs.python.org/3/tutorial/venv.html) so not pollute your system install of Python. Once you create and activate your python environment, use `pip` to install the plugin. Requires Python version &#8805; 3.6.

```bash
pip install mkdocs
pip install mkdocs-versioning
```

???+ tip
    An alternative for managing Virtual Environments is [Anaconda Navigator](https://www.anaconda.com/products/individual) which provides a nice GUI for managing python virtual environments.

## Setup

Once install is complete, use `mkdocs new .` to create an empty mkdocs project. You should then have an `mkdocs.yml` file as well as a `docs/` directory. Now setup `mkdocs.yml` as shown below (**Note**: You can add more to the config if you wish. This is just the minimum):

???+ example
    ```yaml
    edit_uri: ""

    plugins:
    - mkdocs-versioning:
        version: 0.3.0
    nav:
      - Home: "index.md"
      - Version Selector: "../"
    ```
???+ Info "Why is `edit_uri` blank "
    Since the plugin stores the previous versions of the **built** documentation, the diting feature will only allow editing of the current documentation. Attemptin

Write your documentation as normal using `mkdocs serve` to preview your docs as normal. When you run `mkdocs build`, the plugin will:

1. Build your docs into a folder within `site/` and will be named according to the value of `version` (in the example, the docs will be built into `site/0.3.0/`).
2. Remove the old version selection page.
3. Inside `site/` build a new version selection page.

Now when you want to build a new version, simply change the value of `version` (e.g. to 0.4.0) and build again, mkdocs should build the new, updated docs into its own folder and update the version selection page.

???+ Info
    This is just a basic working example, there is more functionality built into the docs such as a having a custom version selection page so it is recommended to read through the entire [details section](reference/index.md) to get a full understanding of how the plugin works in order to take full advantage of the versioning capabilities.