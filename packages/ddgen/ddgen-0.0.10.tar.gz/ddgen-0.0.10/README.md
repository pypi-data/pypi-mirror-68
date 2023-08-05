# ddgen

[![Build Status](https://travis-ci.org/ielis/ddgen.svg?branch=master)](https://travis-ci.org/ielis/ddgen)
[![PyPI version](https://badge.fury.io/py/ddgen.svg)](https://badge.fury.io/py/ddgen)

Library of Python utilities that I needed so many times in the past


## Select RefSeq transcript with the highest priority

RefSeq transcripts have following categories: 
- `NM_`, `XM_`, `NR_`, `XR_`

If we have transcripts from multiple sources, we want to select the one coming from the source with highest priority.
> E.g. `NM_` has higher priority than `XM_`.

If we have multiple transcripts from a single source, we want to select the one with smaller integer.
> E.g. `NM_123.4` has higher priority than `NM_124.4`.

```python
from ddgen.utils import prioritize_refseq_transcripts

# tx will be `NM_123.4`
tx = prioritize_refseq_transcripts(['NM_123.4', 'NM_124.4', 'XM_100.1'])
```


## Get priority for *Jannovar* variant effects

Jannovar assigns one or more effects to a variant. The effects look like
- `MISSENSE_VARIANT`,
- `STOP_GAINED`,
- `SPLICE_DONOR_VARIANT`,
- `CODING_TRANSCRIPT_VARIANT`, etc.

The effects are sorted in order of decreasing putative pathogenicity (i.e. `CODING_TRANSCRIPT_VARIANT` is likely to be less deleterious than `STOP_GAINED` in general).

If the variant affects multiple transcripts, it can have different effects on each of them. In some situations, it might be useful to select and evaluate only the most serious effect.

In order to make the selection, we work with concept of variant effect *priority*. The lower the number representing the priority, the higher the priority.

We can do it by comparing effect priorities:
```python
from ddgen.utils import get_variant_effect_priority, VARIANT_EFFECT_PRIORITIES

# `p` is 21 
p = get_variant_effect_priority('MISSENSE_VARIANT')

# `u` is -1
u = get_variant_effect_priority('GIBBERISH')

# `p` is 21 again
p = VARIANT_EFFECT_PRIORITIES['MISSENSE_VARIANT']
```


## Connect to H2 database

The H2 database is a pure Java SQL database, hence it is primarily meant to be used with Java.
We can connect to the database from Python, if:

- Java is installed on the local machine
- the local machine runs UNIX-like OS (sorry, Windows users)

In that case:
```python
from ddgen.db import H2DbManager

with H2DbManager("path/to/database.mv.db", 
                 user="sa", 
                 password="sa") as h2:
    with h2.get_connection() as conn:
        with conn.cursor() as cur:
            # do whatever you want with the connection/cursor
            cur.execute('SELECT * FROM DB.TABLE;')
            for i, x in zip(range(5), cur.fetchall()):
                # print first 5 lines 
                print(x)
```

## Setup logging

Quick setup of Python built-in `logging` library:

```python
from ddgen.utils import setup_logging
setup_logging()
```
