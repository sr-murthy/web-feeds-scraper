from __future__ import with_statement
from contextlib import closing

import os
import sqlite3
import sys

class FeedsDB(object):

    # No path checking here, assume the files will live in same directory
    # as the scraper and db.py.
    DB_FILE = 'feeds.db'
    DB_SCHEMA = 'schema.sql'

    @classmethod
    def setup(cls):
            if not os.path.exists(cls.DB_FILE):
                print('\n\tDB does not exist, creating DB {} ... '.format(cls.DB_FILE))
                with sqlite3.connect(cls.DB_FILE, timeout=5000) as db:
                    with open(cls.DB_SCHEMA, 'rt') as f:
                       schema = f.read()
                    print('\tcreating DB schema')
                    db.executescript(schema)

    def _insert_row(self, table, columns, values):
        row_id = None
        with sqlite3.connect(self.DB_FILE, timeout=5000) as db:
            with closing(db.cursor()) as cursor:
                cursor.execute(
                    """insert into {} ({}) values ({})""".format(
                        table, ','.join(columns), '{}'.format(','.join(['?'] * len(values)))
                    ),
                    tuple(values)
                )
                # Not necessary, but useful to leave in for unit testing.
                row_id = cursor.lastrowid
            if row_id:
                db.commit()
                return row_id
            else:
                raise Exception('Failed insert into table {}'.format(table))
       
    def save(self, model_inst):
        # Note: I assume that the model field names are identical to the
        # corresponding table column names, with the exception of the
        # '_' prefix. This makes it easier possible to write this method generically.
        table = model_inst.__class__.__name__.lower()
        columns = [attr.strip('_') for attr in list(model_inst.__dict__.keys())]
        values = [val if val else '' for val in [getattr(model_inst, attr) for attr in columns]]
        self._insert_row(table, columns, values)
