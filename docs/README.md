# Generate docs #

1. Generate API docs. [See sphinx-apidoc](http://www.sphinx-doc.org/en/1.5.1/invocation.html#invocation-of-sphinx-apidoc)
````cmd
sphinx-apidoc -o docs sdklib
````

2. Generate html. [See sphinx-build](http://www.sphinx-doc.org/en/1.5.1/invocation.html#invocation-of-sphinx-build)
````cmd
sphinx-build -b html docs/ output/
````