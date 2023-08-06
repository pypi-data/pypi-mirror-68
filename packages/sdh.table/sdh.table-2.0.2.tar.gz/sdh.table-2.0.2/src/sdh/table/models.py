from __future__ import unicode_literals

import pickle
import codecs

from django.db import models
from django.conf import settings
from django.utils import six


class TableViewProfile(models.Model):
    PICKLE_PROTOCOL = 2  # for backwards compatibility with Python2.x

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE, related_name='+')

    tableview_name = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    dump = models.TextField(default='')

    class Meta:
        db_table = 'tableview_profile'

    @property
    def state(self):
        dump = codecs.decode(self.dump, 'hex_codec')
        try:
            return pickle.loads(dump)
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, UnicodeDecodeError):
            pass

        try:
            # Using encoding='latin1' is required for unpickling NumPy arrays
            # and instances of datetime, date and time pickled by Python 2.
            return pickle.loads(dump, encoding="latin1")
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, UnicodeDecodeError):
            pass

    @classmethod
    def dump_state(cls, data):
        dump = pickle.dumps(data, cls.PICKLE_PROTOCOL)
        if six.PY3:
            return codecs.encode(dump, 'hex_codec').decode('ascii')
        return codecs.encode(dump, 'hex_codec')
