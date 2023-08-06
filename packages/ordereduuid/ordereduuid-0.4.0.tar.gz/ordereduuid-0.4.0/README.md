# Ordered UUID

Generates UUIDs ordered by time generated.

## Overview

## Examples
The default constructor generates a UUID using a random multicast MAC
address as the node:

```
>>> from ordereduuid import OrderedUUID
>>> OrderedUUID()
OrderedUUID('1ea96141-1da3-c3ef-e978-ab415e52aca4') 
```

If a private MAC is not preferred, use the set the `private_mac`
keyword argument to `False`:

```
>>> OrderedUUID(private_mac=False)
OrderedUUID('1ea961a5-25a5-c3bf-e26f-ffffffffffff')
```

REQUIRES TESTING/REVIEW -- UUIDs generated are designed to be used as
keys in databases. Consider the following Django example:
```
from django.db import models

from ordereduuid import OrderedUUID

class Subscriber(models.Model):
    id = models.UUIDField(
        primary_key=True, default=OrderedUUID, editable=False
    )
```
