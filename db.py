import os
import sqlite3
import sys

class FeedsDB(object):

    DB_FILE = 'feeds.db'
    DB_SCHEMA = 'schema.sql'

    @classmethod
    def setup(cls):
            if not os.path.exists(cls.DB_FILE):
                print('\tcreating database {} ... '.format(cls.DB_FILE))
                with sqlite3.connect(cls.DB_FILE) as db:
                    with open(cls.DB_SCHEMA, 'rt') as f:
                       schema = f.read()
                    print('\tcreating schema for {} ... '.format(cls.DB_SCHEMA))
                    db.executescript(schema)

    def _insert_row(self, table, columns, values):
        with sqlite3.connect(self.DB_FILE) as db:
            db.execute(
                """insert into {} ({}) values ({})""".format(
                    table, ','.join(columns), '{}'.format(','.join(['?']*len(values)))
                ),
                tuple(values)
            )
            db.commit()

    def save(self, table, model_inst):
        columns = [attr.strip('_') for attr in list(model_inst.__dict__.keys())]
        print('columns={}'.format(columns))
        values = [val if val else '' for val in [getattr(model_inst, attr) for attr in columns]]
        print('values={}'.format(values))
        self._insert_row(table, columns, values)
