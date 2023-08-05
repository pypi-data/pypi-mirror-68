# Multiplexer
---
Multiplexer is an encryption library.

## Installation

```bash
pip install multiplexer
```

## Usage

```python
from multiplexer import Plex, generate, load

book = load() or generate("michel", save=True)

p = Plex(book)

cypher = p.encode('My secret message')

secret_message = p.decode(cypher)
```

## Logging

```python
import logging

logger = logging.getLogger('multiplexer')
logger.setLevel(logging.INFO)
```