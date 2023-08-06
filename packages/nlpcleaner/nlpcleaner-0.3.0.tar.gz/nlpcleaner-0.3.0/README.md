# Nlpcleaner [![Build Status](https://travis-ci.org/giovannelli/nlpcleaner.svg?branch=master)](https://travis-ci.org/giovannelli/nlpcleaner)

Clean and prepare text for modeling with machine learning.
- lower all
- strip all
- remove numbers
- remove symbols
- remove url
- strip html tags
- remove stopwords by detected language
- lemming or stemming

## Usage

```
from nlpcleaner import TextCleaner
TextCleaner(txt).clean()
```

## Tests

```
pipenv install .
python setup.py test
```

## Push on PyPi

```
python setup.py sdist
pip install twine
twine upload dist/*
```

## TODO
* Add tests to cover different cases and languages;
* check performances
