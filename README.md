# Homework #6. Spell checker
## Installation
To install required packages run:

```
pip install -r requirements.txt
```

## Usage
To run monotonic conjugation check run from the project's root:
```
python src/spellcheck.py --word appreceiated -n_suggestions 3
```

You may also run
```
python src/spellcheck.py  --help
```

to see the arguments' description.

## Benchmark
For validation there were used [dataset](http://aspell.net/test/cur/).

Acc@1:   0.492

Acc@5:   0.728

Acc@10:  0.762