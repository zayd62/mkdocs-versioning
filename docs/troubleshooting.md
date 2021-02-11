# Troubleshooting

This page contains common bugs that may occur and how to deal with them

## Combined use of awesome-pages and mkdocs-versioning

In case of using [awesome-pages](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/) the order of registration within the `plugins` is important. The following error may occur:

```python
Traceback (most recent call last):
  [...]
  File "/path/to/mkversion/entry.py", line 47, on_config
    for count, i in enumerate(nav):
TypeError: 'NoneType' object is not iterable
```

You need to make sure, that the `awesome-pages` plugin is registered **after** `mkdocs-versioning`:

```yaml
plugins:
  - mkdocs-versioning:
      version: "1.0"
  - awesome-pages
```

