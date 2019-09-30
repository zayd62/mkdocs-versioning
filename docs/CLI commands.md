# CLI commnads

There are a few CLI commands available. Documentation can be found here as well as through the CLI by running

```
mkdocs-versioning -h
```
## Deploy

```
mkdocs-versioning deploy
```

Used to deploy **already built** docs to [Github Pages](https://pages.github.com/). Note that the docs will need to have
already been built and the command must be executed in the same directory as `mkdocs.yml`

## Sync

```
mkdocs-versioning sync
```
Used to sync the built docs from `gh-pages` into the `site` folder. Primarily used to address [incorrect version 
numbers showing](../Getting Started#correct-version-numbers-not-showing-in-the-version-selection-page). Note that the
command must be executed in the same directory as `mkdocs.yml` and will copy **EVERYTHING** in the `gh-pages` branch 
into the `site` folder