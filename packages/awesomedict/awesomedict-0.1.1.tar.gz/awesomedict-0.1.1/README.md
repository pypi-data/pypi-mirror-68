# INTRODUCTION

A magic dictionary which never raises KeyError but creates non-existent
items as they are requested. By default newly created items in this way are
an empty instance of `AwesomeDict`, but that can be set with `set_defaults`.
The instances also have a `filter` method which can filter based on
a regular expression matched against the key or value. A default regex for
filter can be set with `set_filter`.

# INSTALLATION

`pip install awesomedict`

# EXAMPLE USAGE

```python
from awesomedict import AwesomeDict
import json

# create a default order
mdorder = AwesomeDict().set_defaults(
    {
        '^price$': 0,
        '_address$': 'No such street, PO 000'
    }).set_defaults({'^items$': []}, do_copy=True)
mdorder['items']
mdorder['price']
mdorder['shipping_address']
mdorder['billing_address']

md = AwesomeDict().set_defaults(
    {'^[0-9]+$': mdorder}, do_copy=True).set_filter('^!')
md['customers']['foo'][1]['price'] = 15
md['customers']['foo'][1]['items'].append('notebook')
md['customers']['foo'][1]['shipping_address'] = 'FOO street'
md['customers']['foo'][1]['billing_address'] = 'FOO office'
md['customers']['foo'][1]['!notes'] = 'important notes'
md['customers']['foo'][2]  # use all defaults
md['customers']['!important customer'][1]['price'] = 25  # use default address
md['customers']['!important customer'][1]['items'].append('pen')
print(json.dumps(md, default=lambda o: o.data, indent=2))
print('\n-----important only:-----\n')
print(json.dumps(md.filter(), default=lambda o: o.data, indent=2))
print('\n-----items only:-----\n')
print(json.dumps(md.filter('^items$'), default=lambda o: o.data, indent=2))
```

```
$ python demo.py
{
  "customers": {
    "foo": {
      "1": {
        "items": [
          "notebook"
        ],
        "price": 15,
        "shipping_address": "FOO street",
        "billing_address": "FOO office",
        "!notes": "important notes"
      },
      "2": {
        "items": [],
        "price": 0,
        "shipping_address": "No such street, PO 000",
        "billing_address": "No such street, PO 000"
      }
    },
    "!important customer": {
      "1": {
        "items": [
          "pen"
        ],
        "price": 25,
        "shipping_address": "No such street, PO 000",
        "billing_address": "No such street, PO 000"
      }
    }
  }
}

-----important only:-----

{
  "customers": {
    "foo": {
      "1": {
        "!notes": "important notes"
      }
    },
    "!important customer": {
      "1": {
        "items": [
          "pen"
        ],
        "price": 25,
        "shipping_address": "No such street, PO 000",
        "billing_address": "No such street, PO 000"
      }
    }
  }
}

-----items only:-----

{
  "customers": {
    "foo": {
      "1": {
        "items": [
          "notebook"
        ]
      },
      "2": {
        "items": []
      }
    },
    "!important customer": {
      "1": {
        "items": [
          "pen"
        ]
      }
    }
  }
}
```
