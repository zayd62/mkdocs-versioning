# mkdocs-versioning

`mkdocs-versioning` is a plugin for [mkdocs](https://www.mkdocs.org/), a tool designed to create static websites usually for generating project documentation. 

`mkdocs-versioning` extends mkdocs by differentiating between different versions of documentation you may build. For example, a newer versions of some software may work differently from an older version and it is important that users of an older version of the software reads the appropriate version of the documentation in order to ensure that the user has the correct information and uses the software appropriately.

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-versioning
```

Next, add the following lines to your `mkdocs.yml`:

```yml
plugins:
  - search
  - mkdocs-versioning:
      version: 0.3.0
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Usage

Instructions on how to use the plugin is available at https://zayd62.github.io/mkdocs-versioning/

## Contributing 

Please note that mkdocs-versioning is currently in **Beta** and there may be missing feature/documentation so if you could help out by either:

1. finding and reporting bugs
2. contributing by checking out the [issues](https://github.com/zayd62/mkdocs-versioning/issues)

## Troubleshooting

### Combined use of awesome-pages and mkdocs-versioning

In case of using [awesome-pages](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/) the order of registration within the `plugins` is important. The following error may occur:

```
Traceback (most recent call last):
  [...]
  File "/path/to/mkversion/entry.py", line 47, on_config
    for count, i in enumerate(nav):
TypeError: 'NoneType' object is not iterable
```

You need to make sure, that the `awesome-pages` plugin is register **after** `mkdocs-versioning`:

```yaml
plugins:
  - mkdocs-versioning:
      version: "1.0"
  - awesome-pages
````

