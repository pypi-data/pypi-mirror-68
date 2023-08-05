#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

import re
import logging
from copy import deepcopy
from collections import UserDict
try:
    # python2
    from collections import _abcoll
except ImportError:
    # python3
    from collections import abc as _abcoll


logger = logging.getLogger(__name__)


class AwesomeDict(UserDict, object):
    '''Never raises KeyError, sets the requested key if missing

    The set_defaults and set_filter methods can configure the
    dictionary.

    - set_filter sets the regex used by filter
    - set_defaults is a dictionary of regex--value pairs; the value is
      returned whenever a missing key matching the regex is accessed.
      If a missing key doesn't match any defined default, then a new
      AwesomeDict is returned (and the configuration is copied to it).
    '''

    _default_conf = {'defaults': {}, 'filter_re': None}

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    @property
    def parent(self):
        '''Returns the parent AwesomeDict or None'''

        try:
            return self._parent
        except AttributeError:
            return None

    @property
    def conf(self):
        '''Returns the configuration (defaults and regex filter)'''

        try:
            return self._conf
        except AttributeError:
            if self.parent is None:
                self._conf = deepcopy(self.__class__._default_conf)
            else:
                self._conf = deepcopy(self.parent.conf)
            return self._conf

    def _new_child(self, *args, **kargs):
        child = self.__class__(*args, **kargs)
        child._parent = self
        return child

    def __setitem__(self, key, val):
        if is_dict_like(val):
            md = self._new_child(val)
            return super().__setitem__(key, md)
        if not is_str_like(key):
            raise TypeError(
                ('{} works with keys which are strings and numbers '
                 'as others may not convert to a srting for regex '
                 'matching in an expected way.'.format(
                     self.__class__.__name__)))
        return super().__setitem__(key, val)

    def __getitem__(self, key):
        if not is_str_like(key):
            raise TypeError(
                ('{} works with keys which are strings and numbers '
                 'as others may not convert to a srting for regex '
                 'matching in an expected way.'.format(
                     self.__class__.__name__)))

        try:
            return super().__getitem__(key)
        except KeyError:
            for regex, val_cbk in self.conf['defaults'].items():
                if re.search(regex, str(key)):
                    # val_cbk can return the original value or
                    # a deepcopy of it
                    self[key] = val_cbk()
                    return self[key]
            self[key] = {}  # will be converted to AwesomeDict
            return self[key]

    def filter(self, regex=None):
        '''Filters dictionary based on the given filter

        If regex is None, then the dictionary's default filter (set
        with set_filter) is used, and when another AwesomeDict is found
        as a child, its default filter is used.
        '''

        def _get_filter(regex, default_from):
            if regex is not None:
                return regex
            return default_from.conf['filter_re']

        def _filter(md, empty_is_None=False):
            # create a new empty dictionary of the same parent as md
            if md.parent is None:
                res = md.__class__()
                res.conf.update(md.conf)
            else:
                res = md.parent._new_child()
            for k, v in md.items():
                if re.search(_get_filter(regex, md), str(k)):
                    res[k] = v
                elif isinstance(v, AwesomeDict):
                    f = _filter(v, empty_is_None=True)
                    if f is not None:
                        res[k] = f
                elif re.search(_get_filter(regex, md), str(v)):
                    res[k] = v
            if not res and empty_is_None:
                return None
            return res

        if _get_filter(regex, self) is None:
            return self
        return _filter(self)

    def set_filter(self, regex, append=False):
        '''Updates the filter regex

        - If append is True then the given regex is OR'd with the
          current one (i.e. appended as {current}|{new}.
        Returns the AwesomeDict instance itself.
        '''

        new_filter = regex
        if append:
            curr_filter = self.conf['filter_re']
            if curr_filter is not None:
                new_filter = '{}|{}'.format(curr_filter, new_filter)
        self.conf['filter_re'] = new_filter
        return self

    def set_defaults(self, defaults, do_copy=False, append=True):
        '''Updates the defaults

        - If append is True then the given defaults are added to the
          current ones (default), otherwise they replace them.
        - If do_copy is True, then the values given to keys in
          defaults are deepcopied before being set on new items. This
          option applies only to the values given during this call and
          does not override the setting of previously set defaults.
        Returns the AwesomeDict instance itself.
        '''

        def transformer(obj):
            if do_copy:
                def _callback():
                    return deepcopy(obj)

            else:
                def _callback():
                    return obj

            return _callback

        new_defaults = {}
        if append:
            new_defaults = self.conf['defaults']
        for k, v in defaults.items():
            new_defaults[k] = transformer(v)
        self.conf['defaults'] = new_defaults
        return self

def is_dict_like(val):
    '''True if val is a mutable mapping'''

    # in python2 UserDict is not a child of MutableMapping
    return isinstance(val, (UserDict, _abcoll.MutableMapping))

def is_str_like(val):
    '''True if val can be converted to string straightforwardly

    i.e. if it's a string, boolean or int
    '''

    num_types = (int, float, bool)
    try:  # python2
        str_types = (basestring,)
    except NameError:  # python3
        str_types = (str, bytes)
    return isinstance(val, num_types + str_types)
