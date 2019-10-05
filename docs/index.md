Welcome to mkdocs-versioning
============================

mkdocs-versioning is a plugin for [mkdocs](https://www.mkdocs.org/), a
tool designed to create static websites usually for generating project
documentation. mkdocs-versioning extends mkdocs by differentiating
between different versions of documentation you may build. For example,
a newer versions of some software may work differently from an older
version and it is important that users of an older version of the
software reads the appropriate version of the documentation in order to
ensure that the user has the correct information and uses the software
appropriately.

How does it work
----------------

It works by letting mkdocs build the site normally but builds it into a
folder representing the version the software is assigned (e.g. version
`1.0.0` of the software will be built into a folder labelled `1.0.0`).
The building of the docs is slightly different than usual as there will
be a nav item in ```mkdocs.yml``` called ```Version: ‘../’```. Clicking this will cause
the web browser to move up a directory which will contain an
automatically generated page (built using mkdocs) with links to all the
other versions of the documentation built. The directory structure will
look something like this:

!!! example

    ```    
        ├── 1.0.0
        │   ├── 404.html
        │   ├── assets
        │   ├── circle
        │   ├── index.html
        │   ├── search
        │   ├── sitemap.xml
        │   └── sitemap.xml.gz
        ├── 1.1.0
        │   ├── 404.html
        │   ├── assets
        │   ├── circle
        │   ├── index.html
        │   ├── search
        │   ├── sitemap.xml
        │   ├── sitemap.xml.gz
        │   └── triangle
        ├── 2.0.0
        │   ├── 404.html
        │   ├── assets
        │   ├── circle
        │   ├── index.html
        │   ├── quadrilateral
        │   ├── search
        │   ├── sitemap.xml
        │   ├── sitemap.xml.gz
        │   └── triangle
        ├── 404.html
        ├── assets
        │   ├── fonts
        │   ├── images
        │   ├── javascripts
        │   └── stylesheets
        ├── index.html [1]
        ├── search
        │   └── search_index.json
        ├── sitemap.xml
        └── sitemap.xml.gz 
    ```

This will generate a version selection page with links to version `1.0.0`, `1.1.0` and `2.0.0` of software documentation.
An example version of a built site can be found [here](https://zayd62.github.io/mkdocs-versioning-test/)

!!! note
    **[1]** (the index page in the example above) will contain a single page with links to all versions of the docs that 
    you have built and likewise, all docs that you have built will have link a link to **[1]**


