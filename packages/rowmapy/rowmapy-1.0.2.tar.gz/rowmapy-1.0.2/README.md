# RowmaPy
The Rowma SDK for Python.

## Development
```
$ python setup.py sdist
$ pip install -U .
```

## Publish
```bash
rm -rf dist/*
python setup.py sdist
pip install wheel twine
twine upload dist/*
```
