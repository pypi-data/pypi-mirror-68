## pybackoff

<b>pybackoff</b> is a small c++ optimized implementation of the <i>Stupid Backoff</i> language model for python.
<b>pybackoff</b> uses this language model in combination with 64-bit FNV-1 hash (Fowler-Noll-Vo) for high speed and performance on extremely large datasets.

### Installation
```cmd
$ pip install pybackoff
```

### Example
```python
from pybackoff import SBModel, Ngrams

# get trigram counts and fnv1 hash from corpus
n = Ngrams()
n.load('./data/gutenberg.DAT')

# score trigrams
model = SBModel(n.counts(), n.size())
model.score([('<s>', '<s>', 'this'), ('<s>', 'this', 'is'), ('this', 'is', 'an'), ('is', 'an', 'example')])
```