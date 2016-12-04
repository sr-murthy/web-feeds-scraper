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
        with sqlite3.connect(self.DB_FILE, timeout=5000) as db:
            with closing(db.cursor()) as cursor:
                try:                    
                    statement = """insert into {} ({}) values ({})""".format(
                        table, ','.join(columns), '{}'.format(','.join(['?'] * len(values)))
                    )
                    cursor.execute(
                        statement,
                        tuple(values)
                    )
                except sqlite3.DatabaseError as e:
                    print('\tIN DB: ERROR: {}'.format(str(e)))
                else:
                    db.commit()
                    return cursor.lastrowid
       
    def save(self, model_inst):
        # Note: I assume that the model class names are capitalized versions of
        # the corresponding table names and the model field names are identical to the
        # corresponding table column names after stripping the '_' prefix. This
        # assumption makes it easier to write this method generically and for the
        # scraper calling method to save model instances to the db.
        table = model_inst.__class__.__name__.lower()
        columns = [key.strip('_') for key in model_inst.__dict__]
        values = [model_inst.__dict__[key] if model_inst.__dict__[key] else '' for key in model_inst.__dict__]
        self._insert_row(table, columns, values)
