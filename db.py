from __future__ import with_statement
from contextlib import closing

import os
import sqlite3
import sys

class FeedsDB(object):

    DB_FILE = 'feeds.db'
    DB_SCHEMA = 'schema.sql'

    @classmethod
    def setup(cls):
            if not os.path.exists(cls.DB_FILE):
                print('\n\tcreating database {} ... '.format(cls.DB_FILE))
                with sqlite3.connect(cls.DB_FILE) as db:
                    with open(cls.DB_SCHEMA, 'rt') as f:
                       schema = f.read()
                    print('\tcreating schema for {} ... '.format(cls.DB_FILE))
                    db.executescript(schema)

    def _insert_row(self, table, columns, values):
        row_id = None
        with sqlite3.connect(self.DB_FILE) as db:
            with closing(db.cursor()) as cursor:
                cursor.execute(
                    """insert into {} ({}) values ({})""".format(
                        table, ','.join(columns), '{}'.format(','.join(['?'] * len(values)))
                    ),
                    tuple(values)
                )
                row_id = cursor.lastrowid
                print('\tIN DB: Inserted row #{} into table \'{}\''.format(row_id, table))                
            if row_id:
                db.commit()
                return row_id
            else:
                raise Exception('Failed insert')
       
    def save(self, table, model_inst):
        print('\tIN DB: saving {} to table \'{}\''.format(model_inst, table))
        columns = [attr.strip('_') for attr in list(model_inst.__dict__.keys())]
        values = [val if val else '' for val in [getattr(model_inst, attr) for attr in columns]]
        self._insert_row(table, columns, values)
