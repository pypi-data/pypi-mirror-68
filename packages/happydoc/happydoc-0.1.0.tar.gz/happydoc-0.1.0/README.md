# Happy Doc

## Install

```
$ pip install happydoc
```

## Run

Check available templates:
```
$ happydoc template
['report.md', 'devis.md']
```

Generate a document from template:
```
$ happydoc template report.md myreport.md
```

When report is over convert it to PDF:
```
$ happydoc convert myreport.md myreport.pdf
```

## Read

All documents are generated from the markdown using `python-markdown` syntax and extra extensions.

* https://python-markdown.github.io/extensions/
