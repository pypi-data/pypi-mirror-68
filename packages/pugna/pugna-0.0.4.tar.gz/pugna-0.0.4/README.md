# pugna

Neural Network Fitting Code

## Development

```
conda create -n pugna-dev python=3.7
```

## Uploading to pypi

```
python setup.py clean --all
rm -rf dist/
python3 setup.py sdist bdist_wheel
python3 -m twine upload  dist/*
```
