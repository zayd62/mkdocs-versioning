# How to Use

This page is intended to be a step by step walkthrough on how to use this plugin in a typical environment. This will go through all the available config options as well as CLI commands available when you install this plugin. 

## Version 0.1.0

Lets say, you are building a shape library. `version 0.1.0`  of the documentation is for circles. You want a custom version selection page and you have an `images` directory for images to be used for your docs which needs to be excluded from the version selection page nav (see [here](./index.md#21-why-exclude_from_nav-option) as to why). Your *`mkdocs.yml`* will look something like this:

???+ example "Example *`mkdocs.yml`* for version 0.1.0"
    ```yaml
    plugins:
    - mkdocs-versioning:
        version: 0.1.0
        exclude_from_nav: ["images"]
        version_selection_page: "version_selection.md"
    nav:
      - Home: "index.md"
      - Circle: "circle.md"
      - Version Selector: "../"
    ```

When you run *`mkdocs build`*, your *`site`* directory looks something like this:

???+ example "Example *`site`* directory for version 0.1.0"
    ```yaml
    .
    ├── 0.1.0
    │   ├── ...
    ├── ...
    ```

You then deploy the built docs to **GitHub Pages** using the command *`mkdocs-versioning deploy`*. See [here](cli.md#command-deploy) as to why this plugin has its own deploy command. 

???+ warning
    The *`site`* directory should **NOT** be pushed to any GIT remotes (e.g. GitHub, GitLab, BitBucket etc) and should be ignored using *`.gitignore`* file.

## Version 0.2.0

The next version of the documentation you add documentation for triangles. The updated *`mkdocs.yml`* will look like the following:

???+ example "Example *`mkdocs.yml`* for version 0.2.0"
    ```yaml
    plugins:
    - mkdocs-versioning:
        version: 0.2.0
        exclude_from_nav: ["images"]
        version_selection_page: "version_selection.md"
    nav:
      - Home: "index.md"
      - Circle: "circle.md"
      - Triangle: "triangle.md"
      - Version Selector: "../"
    ```

When you run *`mkdocs build`*, your *`site`* directory now looks something like this:

???+ example "Example *`site`* directory for version 0.2.0"
    ```yaml
    .
    ├── 0.1.0
    │   ├── ...
    ├── 0.2.0
    │   ├── ...
    ├── ...
    ```

You then deploy the built docs to **GitHub Pages** using the command *`mkdocs-versioning deploy`*. 

## Version 0.3.0

The next version of the documentation you add documentation for quadrilateral but, you move to a new computer You perform a *`git clone`* to get a local copy of the repository from your remote but your *`site`* directory is empty since the site is not pushed to the remote (and should not be). You can use *`mkdocs-versioning sync`* which will copy the built docs from GitHub Pages into your *`site`* directory. The *`site`* directory should look exactly the same as the example *`site`* directory for version 0.2.0. 

Once you have a copy of your built docs, your updated *`mkdocs.yml`* will look like the following:

???+ example "Example *`mkdocs.yml`* for version 0.3.0"
    ```yaml
    plugins:
    - mkdocs-versioning:
        version: 0.3.0
        exclude_from_nav: ["images"]
        version_selection_page: "version_selection.md"
    nav:
      - Home: "index.md"
      - Circle: "circle.md"
      - Triangle: "triangle.md"
      - Quadrilateral: "quadrilateral.md
      - Version Selector: "../"
    ```

When you run *`mkdocs build`*, your *`site`* directory now looks something like this:

???+ example "Example *`site`* directory for version 0.3.0"
    ```yaml
    .
    ├── 0.1.0
    │   ├── ...
    ├── 0.2.0
    │   ├── ...
    ├── 0.3.0
    │   ├── ...
    ├── ...
    ```

You then deploy the built docs to **GitHub Pages** using the command *`mkdocs-versioning deploy`*.
