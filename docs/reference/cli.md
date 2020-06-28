# CLI commands

This page will go into the available CLI commands that are available. Run `mkdocs-versioning -h` to access the built in help. 

##  Command: *`deploy`* 

This is used to deploy built docs to GitHub Pages. mkdocs has a built in command for deploying to GitHub Pages but the mkdocs command performs a build before deploying to GitHubs pages which will fail if you have already built the latest version of your docs. Regardless, it is recommended to use *`mkdocs-versioning deploy`*.

##  Command: *`sync`* 

Used to copy the built docs from GitHub pages (By default, the *`gh-pages`* branch).

##  Command: *`unhide`* 

If for whatever reason, during *`mkdocs build`*, it fails, you may have markdown files prefixed with a `*.*`, this command will remove all the `*.*` from all the markdown files (*`.page.md`* --> *`page.md`*). 